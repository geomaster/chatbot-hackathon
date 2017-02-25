$(document).ready(() => {
    let realData =  [
                ["Mobilni uređaji", 30],
                ["Internet", 50],
                ["Roming", 100],
                ["Tarifni paketi", 20],
                ["Računi i ugovori", 120],
                ["Digitalni servisi", 120],
                ["Ostalo", 5]
            ];

    realData = realData.sort((a, b) => a[1] < b[1]);
    let initData = realData.map((x) => [ x[0], 0 ]);

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

    setTimeout(() => {
        chart.load({ columns: realData })
    }, 100);

    $(window).resize(() => {
        chart.resize({
            width: $('#chart').width(),
            height: $('#char').height()
        });
    });

    $.get("/dashboard/api/unanswered_questions.json", (resp) => {
        
    });
});
