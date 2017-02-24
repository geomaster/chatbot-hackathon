function transform(treeMap, node) {
    const result = {};
    for (const k in node) {
        if (k !== "children" && k !== "parent") {
            result[k] = node[k];
        }
    }

    if (node.children) {
        result.children = node.children
            .map((n) => transform(treeMap, treeMap[n]));
    } else {
        result.children = [];
    }

    return result;
}

export function denormalize(pcrtree) {
    const treeMap = {};
    let root = undefined;
    if (!pcrtree.tree) {
        return {}
    }

    for (const node of pcrtree.tree) {
        if (!node.id) {
            continue;
        }

        treeMap[node.id] = node;
        if (!node.parent) {
            root = node;
        }
    }

    return transform(treeMap, root);
}

function transformAndPutIntoMap(treeMap, root, parent) {
    if (root.children) {
        for (const c of root.children) {
            transformAndPutIntoMap(treeMap, c, root);
        }
    }

    let res = {};
    for (const k in root) {
        if (k !== "children") {
            res[k] = root[k];
        }
    }
    res.parent = parent ? parent.id : null;
    res.children = root.children.map((c) => c.id);
    treeMap[root.id] = res;
}

export function normalize(tree) {
    const treeMap = {};
    let res = [];
    transformAndPutIntoMap(treeMap, tree, null);
    for (const k in treeMap) {
        res.push(treeMap[k]);
    }
    console.log(tree);
    return {
        tree: res
    };
}
