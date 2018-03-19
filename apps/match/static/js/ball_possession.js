var origin = [1050/2+80, 680/2+20], scale = 10, cubesData = [], alpha = 0, beta = 0, startAngle = Math.PI/6;
var svg = d3.select('svg').call(d3.drag().on('drag', dragged).on('start', dragStart).on('end', dragEnd)).append('g');
var color = d3.scaleLinear()
  .domain([0, -15])
  .range(["#eeee00", "#ee0000"]);
var cubesGroup = svg.append('g').attr('class', 'cubes');
var mx, my, mouseX, mouseY;
var possessionData, selectedPlayer;

var cubes3D = d3._3d()
    .shape('CUBE')
    .x(function(d){ return d.x; })
    .y(function(d){ return d.y; })
    .z(function(d){ return d.z; })
    .rotateY(startAngle)
    .rotateX(-startAngle)
    .origin(origin)
    .scale(scale);

function selectPlayer(button, team, no) {
  team = team === "home" ? "home" : "away";

  var id = team[0] + no;
  console.log(team+no);
  init(team+no);
}

function processData(data, tt){

    /* --------- CUBES ---------*/

    var cubes = cubesGroup.selectAll('g.cube').data(data, function(d){ return d.id });

    var ce = cubes
        .enter()
        .append('g')
        .attr('class', 'cube')
        .attr('fill', function(d){ return d.height === 0 ? "green" : color(d.height); })
        .attr('stroke', function(d){ return d3.color(color(d.id)).darker(2); })
        .merge(cubes)
        .sort(cubes3D.sort);

    cubes.exit().remove();

    /* --------- FACES ---------*/

    var faces = cubes.merge(ce).selectAll('path.face').data(function(d){ return d.faces; }, function(d){ return d.face; });

    faces.enter()
        .append('path')
        .attr('class', 'face')
        .attr('fill-opacity', 0.95)
        .classed('_3d', true)
        .merge(faces)
        .transition().duration(tt)
        .attr('d', cubes3D.draw);

    faces.exit().remove();
    /* --------- TEXT ---------*/

    var texts = cubes.merge(ce).selectAll('text.text').data(function(d){
        var _t = d.faces.filter(function(d){
            return d.face === 'top';
        });
        return [{height: d.height, centroid: _t[0].centroid}];
    });

    texts
        .enter()
        .append('text')
        .attr('class', 'text')
        .attr('dy', '-.7em')
        .attr('text-anchor', 'middle')
        .attr('font-family', 'sans-serif')
        .attr('font-weight', 'bolder')
        .attr('x', function(d){ return origin[0] + scale * d.centroid.x })
        .attr('y', function(d){ return origin[1] + scale * d.centroid.y })
        .classed('_3d', true)
        .merge(texts)
        .transition().duration(tt)
        .attr('fill', 'black')
        .attr('stroke', 'none')
        .attr('x', function(d){ return origin[0] + scale * d.centroid.x })
        .attr('y', function(d){ return origin[1] + scale * d.centroid.y })
        //.tween('text', function(d){
        //    var that = d3.select(this);
        //    var i = d3.interpolateNumber(+that.text(), Math.abs(d.height));
        //    return function(t){
        //        that.text(i(t).toFixed(1));
        //    };
        //});

    texts.exit().remove();

    /* --------- SORT TEXT & FACES ---------*/

    ce.selectAll('._3d').sort(d3._3d().sort);

}

var grid_size = 5;
var fx = 105 / grid_size;  // x grids

function getX(k) {
  var gx = k%fx;
  return gx * grid_size - 105/2;
}

function getZ(k) {
  var gy = k/fx;
  return gy * grid_size - 68/2;
}

function init(selectedPlayer){
    cubesGroup.selectAll('g.cube').remove();

    cubesData = [];

    var playerData = possessionData[selectedPlayer];
    console.log(playerData);
    for(var k in playerData) {
        var _cube = makeCube(-playerData[k], getX(k), getZ(k));
        _cube.id = 'cube_' + k;
        _cube.height = -playerData[k];
        cubesData.push(_cube);
    }

    processData(cubes3D(cubesData), 1000);
}

function dragStart(){
    mx = d3.event.x;
    my = d3.event.y;
}

function dragged(){
    mouseX = mouseX || 0;
    mouseY = mouseY || 0;
    beta   = (d3.event.x - mx + mouseX) * Math.PI / 230 ;
    alpha  = (d3.event.y - my + mouseY) * Math.PI / 230  * (-1);
    processData(cubes3D.rotateY(beta + startAngle).rotateX(alpha - startAngle)(cubesData), 0);
}

function dragEnd(){
    mouseX = d3.event.x - mx + mouseX;
    mouseY = d3.event.y - my + mouseY;
}

function makeCube(h, x, z){
    return [
        {x: x - 2, y: h, z: z + 2}, // FRONT TOP LEFT
        {x: x - 2, y: 0, z: z + 2}, // FRONT BOTTOM LEFT
        {x: x + 2, y: 0, z: z + 2}, // FRONT BOTTOM RIGHT
        {x: x + 2, y: h, z: z + 2}, // FRONT TOP RIGHT
        {x: x - 2, y: h, z: z - 2}, // BACK  TOP LEFT
        {x: x - 2, y: 0, z: z - 2}, // BACK  BOTTOM LEFT
        {x: x + 2, y: 0, z: z - 2}, // BACK  BOTTOM RIGHT
        {x: x + 2, y: h, z: z - 2}, // BACK  TOP RIGHT
    ];
}

// d3.selectAll('button').on('click', init);

$(document).ready(function() {
  d3.json("../static/data/DFL-MAT-0025I9_bp_gs5.json", function(error, dat) {
    possessionData = dat;
    init(selectedPlayer);
  });
});
