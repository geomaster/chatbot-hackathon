function fromGOJS(gotree) {
	var pcrtree;
	pcrtree.tree = [];

	d = {};

	for(var gonode of gotree.nodeDataArray) {

		d[gonode].id = gonode.name;
		d[gonode].description = node.comment;
		d[gonode].children = [];

		if(gonode.parent) {
			for(var parentgonode of gotree.nodeDataArray) {
				if(parentgonode.key == gonode.parent) {
					d[parentgonode].children.push(gonode.name);
					d[gonode].parent = parentgonode.name;
				}
			}
		}

		d[gonode].entities_needed = gonode.entities_needed;
		d[gonode].entities_refused = gonode.entities_bad;
		d[gonode].message = gonode.message;
	}

	for(var node of d.keys()) {
		pcrtree.tree.push(ndoe);
	}

	return pcrtree;
}

function toGOJS(pcrtree) {
	var cnt = 1;
	var gotree;

	gotree.class = "go.TreeModel";
	gotree.nodeDataArray = [];

	d = {};

	for(var node of pcrtree.tree) {
		d[node].key = cnt++;
		d[node].name = node.id;
		d[node].entities_needed = node.entities_needed;
		d[node].entities_bad = node.entities_refused;
		d[node].message = node.message;

		if(node.parent !== null) {
			for(var parentnode of pcrtree.tree) {
				if(parentnode.name == node.parent) {
					d[node].parent = d[parentnode].key;
				}
			}
		}
	}
}