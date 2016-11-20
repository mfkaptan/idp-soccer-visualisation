/* Global variables */
var teams = {"home": {}, "away": {}};
var ball_data = [];
var index = 0;
var animationPaused = true;
var circles = {"home":{}, "away":{}, "ball":{}};
var slider = null;

function switchState()
{
    if(animationPaused)
        resumeAnimation();
    else
        pauseAnimation();
}

function resumeAnimation()
{
    var btn = document.getElementById("playButton");
    btn.value = "playing";
    btn.innerHTML = '<i class="fa fa-pause"></i>';
    animationPaused = false;
}

function pauseAnimation()
{
    var btn = document.getElementById("playButton");
    btn.value = "paused";
    btn.innerHTML = '<i class="fa fa-play"></i>';
    animationPaused = true;
}

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

function init()
{
    var svg = d3.select("svg");

    for(var player in teams["home"])
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

    for(var player in teams["away"])
    {
        var frame = teams["away"][player][0];

        circles["away"][player] = svg.append("g").attr("transform",
                                                       "translate(" + convertCoordStr(frame.x, frame.y) +")");

        circles["away"][player].append("circle")
                               .attr("r", 10)
                               .attr("stroke", "black")
                               .attr("stroke-width", 2)
                               .style("fill", "red");

        circles["away"][player].append("text")
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

function convertCoord(x, y)
{
    x = x*10 + 575; // 50 + 1050/2 (x offset + half width)
    y = y*10 + 360; // 20 + 680/2 (y offset + half height)

    return [x, y];
};

function convertCoordStr(x, y)
{
    x = x*10 + 575; // 50 + 1050/2 (x offset + half width)
    y = y*10 + 360; // 20 + 680/2 (y offset + half height)

    return " " + x + ", " + y + " ";
}


$(document).ready(function() {

    $("#getData").on('submit', function(event){
        $.ajax({
            type:"GET",
            url:"/DFL-MAT-0025I9/get_data/1/1",
            dataType : "json",
            data: {

            },
            success: function(data){
                teams["home"] = data.home;
                teams["away"] = data.away;
                ball_data = data.ball;
                init();
            }
        });
        event.preventDefault();
    });

    /* Add prev and next methods to array prototype */
    Array.prototype.next = function() {
        return this[++this.current];
    };
    Array.prototype.prev = function() {
        return this[--this.current];
    };
    Array.prototype.current = -1;

    /* Get data */
/*    teams["home"] = ({{data.home | safe }});
    teams["away"] = ({{data.away | safe }});
    ball_data = ({{data.ball | safe }});*/

    slider = $('#seekbar').slider({});

    slider.on("slide", function(slideEvt) {
        pauseAnimation();
        seek(slideEvt.value);
    })

    document.interval = setInterval(function(){
        if(!animationPaused)
        {
            update();
        }
    }, 40);

});
