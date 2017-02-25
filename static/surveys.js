const CATEGORY_MAP = {
    internet: "Internet",
    devices: "Uređaji"
};

let model;

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
            columns: [],
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
            columns: [],
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

    $.get('/dashboard/api/survey_questions.json', (resp) => {
        model = {};
        for (let x in resp) {
            let pie = [];
            for (let ans in resp[x].answers) {
                pie.push([ ans, resp[x].answers[ans] ]);
            }

            let line = [ ["x"] ];
            for (let i = 0; i < 20; i++) {
                line[0].push(i);
            }

            for (let ans in resp[x].answers) {
                let d = [ ans ];
                for (let i = 0; i < 20; i++) {
                    let base = resp[x].answers[ans];
                    base = Math.max(0, base + Math.floor(Math.random() * 20 - 10))
                    d.push(base);
                }

                line.push(d);
            }

            model[resp[x].id] = {
                pie: pie,
                line: line
            };
        }

        function fmt(q) {
            let replies = q.message.quick_replies.map((x) => x.title);
            let repliesHtml = replies.map((x) => `<div class="ui label">${x}</div>`).join('');

            return `<td>${q.message.text}</td><td>${CATEGORY_MAP[q.bucket]}</td><td>${repliesHtml}</td>`;
        }

        $('#survey-question-table-body').html(
            resp.map((x) => `<tr data-id="${x.id}">${fmt(x)}</tr>`)
        );

        $(".survey-questions-table tr:first-child").addClass("selected");
        chart.load({
            unload: true,
            columns: model[resp[0].id].pie
        });
        chartAlt.load({
            unload: true,
            columns: model[resp[0].id].line
        });

        $(".survey-questions-table tr").click(function() {
            let id = $(this).attr("data-id");
            chart.load({
                unload: true,
                columns: model[id].pie
            });

            chartAlt.load({
                unload: true,
                columns: model[id].line,
                x: 'x'
            });

            $(".survey-questions-table tr").removeClass("selected");
            $(this).addClass("selected");
        });

    });
});
