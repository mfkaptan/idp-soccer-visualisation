var circles = {home: {}, away: {}, ball: {}};

function seek(minute)
{
    var lo = 0;
    var hi = ball_data.length;
    var half;

    var loMin = ball_data[lo].m;
    var hiMin = ball_data[hi-1].m;
    // Binary search for minute
    while(hiMin - loMin > 1)
    {
        half = lo + Math.floor((hi - lo) / 2);

        if(ball_data[half].m > minute)
            hi = half;
        else
            lo = half;

        hiMin = ball_data[hi-1].m;
        loMin = ball_data[lo].m;
    }

    // Slide to lo
    var rewind = lo - ball_data.current;
    ball_data.current = lo;

    // Update all arrays
    for(t in teams)  // "home", "away"
    {
        for(var p in teams[t])
        {
            if(teams[t][p].current != -1)
                teams[t][p].current += rewind;

            if(teams[t][p].current < 0)
                teams[t][p].current = -1;
        }
    }

}

var createPath = d3.svg.line()
                       .x(function(d) { return d.x*10 + 575; })
                       .y(function(d) { return d.y*10 + 360; })
                       .interpolate("linear");

function init()
{
    var svg = d3.select("svg");

    d3.json("../static/data/DFL-MAT-0025I9.json", function(error, data) {
        var ball = data.ball;
        var home = data.home;
        var away = data.away;
        delete data;

        svg.append("path").data([ball])
                          .attr("d", createPath)
                          .attr("stroke", "white")
                          .attr("stroke-width", 2)
                          .attr("fill", "none")
                          .attr("id", "ball");

/*        for(var player in home)
        {
            svg.append("path").data([home[player]])
                              .attr("d", createPath)
                              .attr("stroke", "blue")
                              .attr("stroke-width", 1)
                              .attr("fill", "none")
                              .attr("stroke-dasharray", "0 0")
                              .attr("id", "h" + player);
        }

        for(var player in away)
        {
            svg.append("path").data([away[player]])
                              .attr("d", createPath)
                              .attr("stroke", "red")
                              .attr("stroke-width", 1)
                              .attr("fill", "none")
                              .attr("stroke-dasharray", "0 0")
                              .attr("id", "a" + player);
        }*/
    });

/*
    var path = d3.select("#ball");
    var len = path.node().getTotalLength();
    path.attr("stroke-dasharray", len + " " + len)
        .attr("stroke-dashoffset", len);

    console.log(d3.select("path#ball"));
*/
};

function update() {
    var ballFrame = ball_data.next();
    if(!ballFrame)
    {
        pauseAnimation();
        ball_data.prev();
        return;
    }

    var currentFrame = ballFrame.n;

    if(slider.data('slider').getValue() != ballFrame.m)
        slider.data('slider').setValue(ballFrame.m);

    xy = convertCoord(ballFrame.x, ballFrame.y);
    circles["ball"].attr("cx", xy[0]).attr("cy", xy[1]).attr("r", 4+ballFrame.z/8);

    for(t in teams)  // "home", "away"
    {
        for(var p in teams[t])
        {
            var frame = teams[t][p].next(); //[index];

            if(frame)
            {
                if(frame.n == currentFrame)
                {
                    // In the game, update
                    circles[t][p].attr("transform",
                                       "translate(" + convertCoordStr(frame.x, frame.y) + ")");
                }
                else
                {
                    // Not in the game yet
                    teams[t][p].prev();
                }
            }
            else
            {
                // Substituted
                if(t == "home")
                    circles[t][p].attr("transform", "translate(20,700)");
                else
                    circles[t][p].attr("transform", "translate(1130,700)");

            }
        }
    }
}


$(document).ready(function() {
    init();

    /* Add prev and next methods to array prototype */
    Array.prototype.next = function() {
        return this[++this.current];
    };
    Array.prototype.prev = function() {
        return this[--this.current];
    };
    Array.prototype.current = -1;
});

/*    for(var player in teams["home"])
    {
        var frame = teams["home"][player][0];

        circles["home"][player] = svg.append("g").attr("transform",
                                                       "translate(" + convertCoordStr(frame.x, frame.y) +")");

        circles["home"][player].append("circle")
                               .attr("r", 10)
                               .attr("stroke", "black")
                               .attr("stroke-width", 2)
                               .style("fill", "steelblue");

        circles["home"][player].append("text")
                               .style("font-family", "Times New Roman")
                               .style("font-size", 14)
                               .style("fill", "white")
                               .attr("text-anchor", "middle")
                               .attr("alignment-baseline", "middle")
                               .text(player);

    }

    circles["ball"] = svg.append("circle").attr("cx", 50 + 1050/2).attr("cy", 20 + 680/2)
                                                                  .attr("r", 4)
                                                                  .attr("fill", "white");
*/
