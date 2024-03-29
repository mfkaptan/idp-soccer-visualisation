"use strict";

var ball = {},
  home = {},
  away = {},
  opac = {};
var circles = { home: {}, away: {}, ball: {} };
var fromMin = 0,
  fromSec = 0;
var toMin = 0,
  toSec = 15;

var createPath = d3.svg.line()
  .x(function(d) { return d.x * 10 + 575; })
  .y(function(d) { return d.y * 10 + 360; })
  .interpolate("linear");


function convertCoord(x, y) {
  x = x * 10 + 575; // 50 + 1050/2 (x offset + half width)
  y = y * 10 + 360; // 20 + 680/2 (y offset + half height)
  return "" + x + "," + y;
}


function draw() {
  var from = Math.round(fromMin) * 60 * 25 + Math.round(fromSec) * 25;
  var to = Math.round(fromMin) * 60 * 25 + Math.round(toSec) * 25;
  var svg = d3.select("#field");

  d3.selectAll(".ball-path").remove();
  d3.selectAll(".home-path").remove();
  d3.selectAll(".away-path").remove();

  /* Ball */
  var data = ball.slice(from, to);
  var frame = data[data.length - 1];

  svg.append("path").data([data])
    .attr("d", createPath)
    .attr("stroke", "white")
    .attr("stroke-width", 2)
    .attr("fill", "none")
    .attr("class", "ball-path")
    .attr("id", "ball");

  circles["ball"].attr("cx", frame.x * 10 + 575)
    .attr("cy", frame.y * 10 + 360)
    .attr("r", 4 + frame.z / 8);

  var player, id;
  for (player in home) {
    id = "h" + player;
    data = home[player].slice(from, to);
    frame = data[data.length - 1];
    svg.append("path").data([data])
      .attr("d", createPath)
      .attr("stroke", "blue")
      .attr("stroke-width", 1)
      .attr("fill", "none")
      .attr("stroke-dasharray", "0 0")
      .attr("class", "away-path")
      .attr("id", "h" + player)
      .attr("opacity", opac[id]);
    circles["home"][player].attr("opacity", opac[id])
      .attr("transform", "translate(" + convertCoord(frame.x, frame.y) + ")")
  }

  for (player in away) {
    id = "a" + player;
    data = away[player].slice(from, to);
    frame = data[data.length - 1];
    svg.append("path").data([data])
      .attr("d", createPath)
      .attr("stroke", "red")
      .attr("stroke-width", 1)
      .attr("fill", "none")
      .attr("stroke-dasharray", "0 0")
      .attr("class", "away-path")
      .attr("id", id)
      .attr("opacity", opac[id]);
    circles["away"][player].attr("opacity", opac[id])
      .attr("transform", "translate(" + convertCoord(frame.x, frame.y) + ")")
  }
}


function initSliders() {
  var minSlider = $("#minSlider");
  var secSlider = $("#secSlider");
  minSlider.rangeSlider({
    bounds: { min: 0, max: 50 },
    defaultValues: { min: 0, max: 3 },
    step: 1
  });

  minSlider.bind("valuesChanged", function(e, data) {
    fromMin = data.values.min;
    toMin = data.values.max;
    secSlider.rangeSlider("option", "bounds", { min: 0, max: (toMin - fromMin + 1) * 60 });
    draw();
  });

  secSlider.rangeSlider({
    bounds: { min: 0, max: 180 },
    defaultValues: { min: 0, max: 15 },
    range: { min: 1, max: false },
    step: 1
  });

  secSlider.bind("valuesChanging", function(e, data) {
    fromSec = data.values.min;
    toSec = data.values.max;
    draw();
  });
}


function initCircles() {
  var svg = d3.select("#field");
  var player, frame;

  for (player in home) {
    opac["h" + player] = 1; // Set opacity
    frame = home[player][0];

    circles["home"][player] = svg.append("g")
      .attr("transform",
        "translate(" + convertCoord(frame.x, frame.y) + ")");

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

  for (player in away) {
    opac["a" + player] = 1; // Set opacity
    frame = away[player][0];

    circles["away"][player] = svg.append("g")
      .attr("transform",
        "translate(" + convertCoord(frame.x, frame.y) + ")");

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

  circles["ball"] = svg.append("circle").attr("cx", 50 + 1050 / 2)
    .attr("cy", 20 + 680 / 2)
    .attr("r", 4)
    .attr("fill", "white");
}


function togglePath(button, team, no) {
  team = team === "home" ? "home" : "away";

  var id = team[0] + no;
  var p = d3.select("path#" + id);

  //noinspection EqualityComparisonWithCoercionJS
  if (p.style("opacity") == 0) { // Toggle ON
    opac[id] = 1;
    circles[team][no].attr("opacity", 1);
    p.style("opacity", 1);
    button.addClass('list-group-item-success');
  } else { // Toggle OFF
    opac[id] = 0;
    circles[team][no].attr("opacity", 0);
    p.style("opacity", 0);
    button.removeClass('list-group-item-success');
  }
}


$(document).ready(function() {
  d3.json("../static/data/DFL-MAT-0025I9.json", function(error, data) {
    ball = data.ball;
    home = data.home;
    away = data.away;
    initCircles();
    draw();
  });

  initSliders();

  /* Add prev and next methods to array prototype */
  Array.prototype.next = function() {
    return this[++this.current];
  };
  Array.prototype.prev = function() {
    return this[--this.current];
  };
  Array.prototype.current = -1;
});


/*function update() {
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
                                       "translate(" + convertCoord(frame.x, frame.y) + ")");
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
*/
