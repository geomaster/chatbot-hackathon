function fromGOJS(gotree) {
	var pcrtree = {};
	pcrtree.tree = [];

	d = {};

	for(var gonode of gotree.nodeDataArray) {

		d[gonode.key] = {}
		d[gonode.key].id = gonode.name;
		d[gonode.key].children = [];

		if(gonode.parent) {
			for(var parentgonode of gotree.nodeDataArray) {
				if(parentgonode.key == gonode.parent) {
					d[parentgonode.key].children.push(gonode.name);
					d[gonode.key].parent = parentgonode.name;
				}
			}
		}

		var jsonObject = JSON.parse(gonode.json);
		for (var k in jsonObject) {
			d[gonode.key][k] = jsonObject[k];
		}
	}

	for(var key in d) {
		pcrtree.tree.push(d[key]);
	}

	return pcrtree;
}

function toGOJS(pcrtree) {
	var cnt = 1;
	var gotree = {};

	gotree.class = "go.TreeModel";
	gotree.nodeDataArray = [];

	d = {};

	for(var node of pcrtree.tree) {

		d[node.id] = {}
		d[node.id].key = cnt++;
		d[node.id].name = node.id;
		d[node.id].json = JSON.stringify({
			entities_needed: node.entities_needed,
			entities_refused: node.entities_refused,
			message: node.message,
			description: node.description
		}, undefined, 4);
		d[node.id].entities_bad = node.entities_refused;
		d[node.id].message = node.message;

		if(node.parent !== null) {
			for(var parentnode of pcrtree.tree) {
				if(parentnode.id == node.parent) {
					d[node.id].parent = d[parentnode.id].key;
				}
			}
		}

		if(node.message.text) {
			d[node.id].message_text = node.message.text;
		}
		if(node.message.quick_replies) {
			d[node.id].quick_replies = node.message.quick_replies.map(function(x) { return x.title }).join(", ");
		}
	}

	for(var key in d) {
		gotree.nodeDataArray.push(d[key]);
	}

	return gotree;
}