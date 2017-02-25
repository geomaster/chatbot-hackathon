const CATEGORY_MAP = {
    internet: "Internet",
    devices: "Uređaji"
};

$(document).ready(() => {
    let initData = [];

    let chart = c3.generate({
        bindto: "#chart",
        color: {
            pattern: [
                "#db2828",
                "#f2711c",
                "#fbbd08",
                "#b5cc18",
                "#21ba45",
                "#00b5ad",
                "#2185d0",
                "#6435c9"
            ]
        },
        transition: {
            duration: 900
        },
        size: {
            width: $('#chart').width(),
            height: $('#chart').width()
        },
        data: {
            columns: initData,
            type: "pie"
        }
    });

    $.get("/dashboard/api/by_categories.json", (resp) => {
        let data = [];
        let initData = [];
        for (let k in resp) {
            c = CATEGORY_MAP[k];
            data.push([c, resp[k]]);
            initData.push([c, 0]);
        }
        chart.load({ columns: initData });
        setTimeout(() => {
            chart.load({ columns: data });
        }, 100);
    });

    $(window).resize(() => {
        chart.resize({
            width: $('#chart').width(),
            height: $('#char').height()
        });
    });

    function refresh() {
        $.get("/dashboard/api/unanswered_questions.json", (resp) => {
            $('#unanswered-questions-body').html(
                resp.map((x) =>
                    `<tr data-id="${x.id}"><td>${x.text}</td><td>${CATEGORY_MAP[x.category] || "Nepoznato"}</td>`
                ).join('')
            );
        });
    }

    refresh();
    setInterval(refresh, 500);
});
