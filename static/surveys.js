$(document).ready(() => {
    function randomData() {
        let pie = [];
        let line = [
            ["x"],
            ["Da"],
            ["Ne"],
            ["Mozda"]
        ];

        let ansMap = [ "Da", "Ne", "Mozda" ];

        for (let i = 10; i < 20; i++) {
            line[0].push(i);
        }

        for (let ans = 0; ans < 3; ans++) {
            for (let i = 10; i < 20; i++) {
                line[ans + 1].push(Math.floor(Math.random() * 10));
            }

            pie.push([ ansMap[ans], Math.random() * 100 ]);
        }

        console.log(line);
        return {
            pie: pie,
            line: line
        };
    };

    let keys = [
        1, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3
    ];

    let data = {};
    keys.map((k) => data[k] = randomData());

    let chart = c3.generate({
        bindto: "#chart",
        transition: {
            duration: 700
        },
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
        size: {
            width: $('#chart').width(),
            height: $('#chart').width()
        },
        data: {
            columns: data["1"].pie,
            type: "pie"
        }
    });

    let chartAlt = c3.generate({
        bindto: "#chart-alt",
        transition: {
            duration: 700
        },
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
        size: {
            width: $('#chart-alt').width(),
            height: $('#chart-alt').width()
        },
        data: {
            x: 'x',
            columns: data["1"].line,
            type: "line"
        }
    });

    $('#global-view a').click(() => {
        $('#pie-tab').fadeIn(400);
        $('#line-tab').fadeOut(400);

        $('#global-view').addClass("active");
        $('#time-view').removeClass("active");
    });

    $('#time-view a').click(() => {
        $('#line-tab').fadeIn(400);
        $('#pie-tab').fadeOut(400);

        $('#global-view').removeClass("active");
        $('#time-view').addClass("active");

        chartAlt.resize({
            width: $('#chart-alt').width(),
            height: $('#chart-alt').height()
        });
    });

    $(".survey-questions-table tr").click(function() {
        let id = $(this).attr("data-id");
        chart.load({
            columns: data[id].pie
        });

        chartAlt.load({
            columns: data[id].line,
            x: 'x'
        });

        $(".survey-questions-table tr").removeClass("selected");
        $(this).addClass("selected");
    });
});
