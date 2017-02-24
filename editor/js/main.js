import "../sass/main.scss"
import { normalize, denormalize } from "./tree"
import { COLORS } from "./colors"

let treeInfo = {};

const NODE_WIDTH = 330;
const NODE_HEIGHT = 190;
const NODE_PADDING_X = 120;
const NODE_PADDING_Y = 50;
let currentlySelected = null;
let newlyCreated = null;
let mymonaco;


function updateEditor() {
    if (currentlySelected) {
        mymonaco.getModel().setValue(nodeToJson(currentlySelected.data));
    }
}


// fuck javascript
Object.map = function(o, f, ctx) {
    ctx = ctx || this;
    var result = [];
    Object.keys(o).forEach(function(k) {
        result.push(f.call(ctx, o[k], k, o));
    });
    return result;
}

function nodeToJson(node) {
    return JSON.stringify({
        id: node.id,
        description: node.description,
        message: node.message,
        entities_needed: node.entities_needed,
        entities_refused: node.entities_refused
    }, undefined, 4);
}

function init(treeData) {
    let width = document.getElementById("main-canvas").offsetWidth,
        height = document.getElementById("main-canvas").offsetHeight;

    let svg = d3.select("#main-canvas").append("svg")
        .call(d3.zoom().on("zoom", function () {
            let t = d3.event.transform;
            svg.attr("transform", `translate(${t.x}, ${t.y}), scale(${t.k})`);
        }))
        .append("g");

    var i = 0,
        duration = 200,
        root;

    // declares a tree layout and assigns the size
    var treemap = d3.tree().nodeSize([NODE_WIDTH + NODE_PADDING_X, NODE_HEIGHT + NODE_PADDING_Y]);

    // Assigns parent, children, height, depth
    root = d3.hierarchy(treeData, function(d) { return d.children; });

    root.x0 = 0;
    root.y0 = 0;

    update(root);

    // Collapse the node and all it's children
    function collapse(d) {
        if(d.children) {
            d._children = d.children
            d._children.forEach(collapse)
            d.children = null
        }
    }

    let maxChildrenAtLevel = {};
    function getHeightOffset(d) {
        let res = 0;
        for (let x = d.depth; x >= 0; x--) {
            res += maxChildrenAtLevel[x];
        }

        return res;
    }

    function formatEntitiesList(entityList) {
        return Object.map(entityList, (e, k) => {
            if (!(e instanceof Array) || e.length === 0) {
                return k;
            } else {
                return k + " = " + e.join(" | ");
            }
        }).join(", ")
    }

    function formatEntities(node) {
        let s = [];
        if (node.entities_needed && Object.keys(node.entities_needed).length > 0) {
            s.push("+ " + formatEntitiesList(node.entities_needed));
        }
        if (node.entities_refused && Object.keys(node.entities_refused).length > 0) {
            s.push("- " + formatEntitiesList(node.entities_refused));
        }

        return s.join("\n");
    }

    function update(source) {

        // Assigns the x and y position for the nodes
        var treeData = treemap(root);

        // Compute the new tree layout.
        var nodes = treeData.descendants().reverse();
        maxChildrenAtLevel = {};
        nodes.forEach((d) => {
            let myParentChildCount = treeInfo[treeInfo[d.data.id].parent].childrenCount;
            maxChildrenAtLevel[d.depth] = Math.max(maxChildrenAtLevel[d.depth] ? maxChildrenAtLevel[d.depth] : 0, myParentChildCount);
        });
        nodes.forEach((d) => {
            if (d && newlyCreated == d.data.id) {
                newlyCreated = null;
                select(d);
            }
        });
        nodes.forEach(function(d){ d.y += height/2 + getHeightOffset(d) * 40; d.x += width / 2; });
        let links = treeData.descendants().slice(1);

        nodes.forEach(function(d){
            if (d && !d.x0) {
                d.x0 = 100;
                d.y0 = 100;
            }
        });

        // Normalize for fixed-depth.

        // ****************** Nodes section ***************************

        // Update the nodes...
        var node = svg.selectAll('g.node')
            .data(nodes, function(d) {return d.id || (d.id = ++i); });

        // Enter any new modes at the parent's previous position.
        var nodeEnter = node.enter().append('g')
            .attr('class', 'node')
            .attr("transform", function(d) {
                return "translate(" + source.x0 + "," + source.y0 + ")";
            })
            .on('dblclick', click)
            .on('click', select)
            .on('contextmenu', select);

        // Add Circle for the nodes
        nodeEnter.append('rect')
            .attr('class', 'node')
            .attr('width', NODE_WIDTH)
            .attr('height', NODE_HEIGHT)
            .attr('transform', `translate(-${NODE_WIDTH / 2}, -${NODE_HEIGHT / 2})`)
            .style("fill", function(d) {
                return d.selected ? "#fff" : COLORS[d.depth % COLORS.length];
            })
            .style("fill-opacity", 1)

        // Add labels for the nodes
        let nodeInfo = nodeEnter.append("foreignObject")
            .attr("width", NODE_WIDTH)
            .attr("height", NODE_HEIGHT)
            .attr("transform", `translate(-${NODE_WIDTH / 2}, -${NODE_HEIGHT / 2})`)
            .append("xhtml:body")
            .attr("class", "nodeInfoBody")
            .append("div")
            .attr("class", "nodeInfo")
            .append("div");

        nodeInfo.append("div")
            .attr("class", "nodeInfoTitle")

        nodeInfo.append("div")
            .attr("class", "nodeInfoMessage")

        nodeInfo.append("div")
            .attr("class", "nodeInfoQuickReplies")
            .append("ul")
            .attr("class", (d) => `myUl-${d.data.id}`);

        $('.nodeInfoQuickReplies ul').each(function() {
            let id = this.className.replace('myUl-', '');
            let d = treeInfo[id].obj;
            $(this).html(d.message.quick_replies ? "<li>" + d.message.quick_replies.map((qr) => qr.title).join("</li><li>") +  "</li>" : "" );
        });

        // UPDATE
        var nodeUpdate = nodeEnter.merge(node).transition().duration(duration);

        // Transition to the proper position for the node
        nodeUpdate.attr("transform", function(d) { 
                return "translate(" + d.x + "," + d.y + ")";
            });

        nodeUpdate.select('rect')
            .style('fill', (d) => d.selected ? "#fff" : COLORS[d.depth % COLORS.length]);

        nodeUpdate.select('foreignObject body')
            .attr('class', (d) => d.selected ? "nodeInfoBody selected" :"nodeInfoBody");

        nodeUpdate.select('.nodeInfoMessage')
            .text((d) => { return d.data.message.text });

        nodeUpdate.select('.nodeInfoTitle')
            .text((d) => { return d.data.id });

        nodeUpdate.select('.nodeInfoQuickReplies ul')
           // .html((d) => { return d.data.message.quick_replies ? "<li>" + d.data.message.quick_replies.map((qr) => qr.title).join("</li><li>") +  "</li>" : "" });

        // Remove any exiting nodes
        var nodeExit = node.exit().transition()
            .duration(duration)
            .attr("transform", function(d) {
                return "translate(" + source.x + "," + source.y + ")";
            })
            .remove();

        nodeExit.select('rect')
            .attr('fill-opacity', 0);

        // ****************** links section ***************************

        // Update the links...
        var link = svg.selectAll('g.link')
            .data(links, function(d) { return d.id; });

        // Enter any new links at the parent's previous position.
        var linkEnter = link.enter().append("g").attr("class", "link");

        let linkPath = linkEnter.append('path')
            .attr("class", "link")
            .attr('d', function(d){
                var o = {x: source.x, y: source.y};
                return diagonal(o, o, 0, 1);
            });

        let linkText = linkEnter.append("text")
            .attr("font-family", "Arial, Helvetica, sans-serif")
            .attr("fill", "Black")
            .style("font", "normal 12px Arial")
            .attr("class", "linkLabel")
            .attr("transform", function(d) {
                return "translate(" +
                    ((d.x + d.parent.x)/2) + "," +
                    ((d.y + d.parent.y)/2) + ")";
            })
            .attr("dy", ".35em")
            .attr("text-anchor", "middle");


        // UPDATE
        var linkUpdate = linkEnter.merge(link);

        // Transition back to the parent element position
        linkUpdate.select('path').transition()
            .duration(duration)
            .attr('d', function(d){ 
                return diagonal(d, d.parent, treeInfo[d.parent.data.id].childIndex[d.data.id], treeInfo[d.parent.data.id].childrenCount)
            });

        linkUpdate.select('text').transition().duration(duration)
            .attr('transform', function(d){ 
                return "translate(" +
                    ((d.x + d.parent.x)/2) + "," +
                    ((d.y + d.parent.y)/2) + ")";
            })
            .text((d) => formatEntities(d.data));

        // Remove any exiting links
        var linkExit = link.exit().transition()
            .duration(duration).remove();

        linkExit.select('path')
            .attr('d', function(d) {
                var o = {x: source.x, y: source.y};
                return `M ${o.x} ${o.y}
                        L ${o.x} ${o.y}`;
            })
            .remove();

        linkExit.select('text')
            .duration(duration)
            .attr("transform", (d) => `translate(${source.x}, ${source.y})`)
            .remove();

        // Store the old positions for transition.
        nodes.forEach(function(d){
            d.x0 = d.x;
            d.y0 = d.y;
        });

        // Creates a curved (diagonal) path from parent to the child nodes
        function diagonal(s, d, childIdx, childCount) {

            let path = `M ${s.x} ${s.y - NODE_HEIGHT/2}
                        L ${d.x + ((childIdx + 0.5) / childCount - 0.5) * NODE_WIDTH} ${d.y + NODE_HEIGHT/2}`

            return path;
        }

        // Toggle children on click.
        function click(d) {
            if (d.children) {
                d._children = d.children;
                d.children = null;
            } else {
                d.children = d._children;
                d._children = null;
            }
            update(d);

            return false;
        }

        function select(d, noUpdate) {
            console.log("ogilog ");
            d.selected = true;
            if (currentlySelected) {
                currentlySelected.selected = false;
            }
            currentlySelected = d;
            if (!noUpdate) {
                update(d);
            }
            updateEditor();

            return false;
        }
    }

    let counter = 1;

    $(document).ready(() => {
        console.log('reeady');
        $('.add-node-btn').click(() => {
            if (currentlySelected) {
                let newId = `NEW_NODE_${counter++}`;
                currentlySelected.data.children.push({
                    id: newId,
                    children: [],
                    entities_needed: { "intent": [ "some_intent" ] },
                    entities_refused: {},
                    message: {},
                    description: "",
                    parent: currentlySelected.data.id
                });
                treeInfo[newId] = {
                    childIndex: {},
                    childrenCount: 0,
                    parent: currentlySelected.data.id
                };
                newlyCreated = newId;
                updateTreeInfo(treeInfo[currentlySelected.data.id].parent, currentlySelected.data)
                root = d3.hierarchy(treeData, function(d) { return d.children; });
                update(root);
            }
        });

        $('.remove-node-btn').click(() => {
            if (currentlySelected) {
                let parent = treeInfo[treeInfo[currentlySelected.data.id].parent].obj;
                parent.children = parent.children.filter((c) => c.id !== currentlySelected.data.id);
                updateTreeInfo(treeInfo[parent.id].parent, parent);
                root = d3.hierarchy(treeData, function(d) { return d.children; });
                update(root);
            }
        });


        $('.edit-node-btn').click(() => {
            $('#editor').toggleClass('active');
            updateEditor();
        });

        $('.save-btn').click(() => {
            let data = JSON.stringify(normalize(treeInfo["START"].obj), undefined, 4);
            $.ajax({
                type: "PUT",
                url: "/api/graph.json",
                contentType: "application/json",
                data
            }).then((resp) => {
                alert("Saved. Response:\n" + JSON.stringify(resp, null, 2));
            });
        });

        $('#main-canvas').contextmenu((e) => {
            e.preventDefault();
            return false;
        });

        window.require.config({ paths: { 'vs': 'monaco/min/vs' }});
        window.require(['vs/editor/editor.main'], function() {
            var editor = monaco.editor.create(document.getElementById('editor'), {
                value: [
                    '{',
                    '}'
                ].join('\n'),
                language: 'json'
            });

            let updateTimeout = null;

            mymonaco = editor;
            editor.getModel().onDidChangeContent((e) => {
                if (updateTimeout) {
                    clearTimeout(updateTimeout);
                }

                updateTimeout = setTimeout(() => {
                    let text = editor.getModel().getValue();
                    if (currentlySelected) {
                        let d = currentlySelected.data;
                        try {
                            let json = JSON.parse(text);
                            d.message = json.message;
                            d.description = json.description;
                            d.entities_needed = json.entities_needed;
                            d.entities_refused = json.entities_refused;

                            let toUpdate = currentlySelected;
                            if (!treeInfo[json.id]) {
                                treeInfo[json.id] = treeInfo[d.id];
                                for (const c of d.children) {
                                    treeInfo[c.id].parent = json.id;
                                }
                                let parentInfo = treeInfo[treeInfo[json.id].parent];
                                parentInfo.childIndex[json.id] = parentInfo.childIndex[d.id];
                                delete parentInfo[d.id];
                                delete treeInfo[d.id];
                                $(`.myUl-${d.id}`)[0].className = `myUl-${json.id}`;
                                d.id = json.id;
                            }
                            update(toUpdate.parent);
                        } catch (e) {
                            console.log(e);
                        }
                    }
                }, 500);
            })
        });
    });
}

function updateTreeInfo(parent, root) {
    treeInfo["none"] = { childrenCount: 0 }
    treeInfo[root.id] = {
        childIndex: {},
        childrenCount: root.children ? root.children.length : 0,
        parent: parent || "none",
        obj: root
    };

    if (root.children) {
        let i = 0;
        for (const c of root.children) {
            treeInfo[root.id].childIndex[c.id] = i++;
            updateTreeInfo(root.id, c);
        }
    }
}

d3.json("/api/graph.json", function(err, treeData) {
    let denom = denormalize(treeData);
    updateTreeInfo(null, denom);
    init(denom);
});

