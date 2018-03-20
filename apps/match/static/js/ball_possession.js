var origin = [1050/2+60, 680/2+20], scale = 10, alpha = 0, beta = 0, startAngle = Math.PI/8;
var svg = d3.select('svg').call(d3.drag().on('drag', dragged).on('start', dragStart).on('end', dragEnd)).append('g');
var color = d3.scaleLinear()
  .domain([0, -3])
  .range(["#eeee00", "#ee0000"]);
var cubesGroup = svg.append('g').attr('class', 'cubes');
var linesGroup = svg.append('g').attr('class', 'lines');
var mx, my, mouseX, mouseY;
var possessionData, selectedPlayer="home1", selectedHalf="firstHalf", selectedGridSize=2;
var key = function(d){ return d.id; };
var cubesData = [], planeData = [], linesData = [];

var plane3D = d3._3d()
    .shape('PLANE')
    .origin(origin)
    .rotateY(-Math.PI/8)
    .rotateX(-Math.PI/5)
    .scale(scale);

var lines3D = d3._3d()
    .shape('LINE_STRIP')
    .origin(origin)
    .rotateY(-Math.PI/8)
    .rotateX(-Math.PI/5)
    .scale(scale);

var cubes3D = d3._3d()
    .shape('CUBE')
    .x(function(d){ return d.x; })
    .y(function(d){ return d.y; })
    .z(function(d){ return d.z; })
    .rotateY(-Math.PI/8)
    .rotateX(-Math.PI/5)
    .origin(origin)
    .scale(scale);

function selectPlayer(button, team, no) {
  team = team === "home" ? "home" : "away";

  var id = team[0] + no;
  console.log(team+no);
  selectedPlayer = team+no;
  init();
}

function selectHalf(half) {
  selectedHalf = half;
  init();
}

function selectGridSize(gridSize) {
  selectedGridSize = gridSize;
  loadData();
}

function selectDomain(domain) {
  color = d3.scaleLinear()
  .domain([0, -domain])
  .range(["#eeee00", "#ee0000"]);
  init();
}

function processData(data, planeData, lineData, tt){
    /* ----------- PLANE ----------- */

    var plane = svg.selectAll('path.plane').data(planeData, key);

    plane
        .enter()
        .append('path')
        .attr('class', '_3d plane')
        .merge(plane)
        .attr('stroke', 'black')
        .attr('stroke-width', 0.3)
        .attr('fill', function(d){ return d.ccw ? 'lightgreen' : 'darkgreen'; })
        .attr('fill-opacity', 0.1)
        .attr('d', plane3D.draw);

    plane.exit().remove();

    /* ----------- LINES ----------- */

    var lines = linesGroup.selectAll('g.lines').data(lineData);

    lines
      .enter()
      .append('g')
      .attr('class', 'lines-cls')
      .append('path')
      .merge(lines)
      .attr('stroke', 'white')
      .attr('fill', 'white')
      .attr('stroke-width', 2)
      .attr('fill-opacity', 0.1)
			.attr('d', lines3D.draw);

    lines.exit().remove();

    /* --------- CUBES ---------*/

    var cubes = cubesGroup.selectAll('g.cube').data(data, key);

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

function getX(k) {
  var fx = Math.floor(105 / selectedGridSize);  // x grids
  var gx = k%fx;
  return gx * selectedGridSize - 110/2;
}

function getZ(k) {
  var fx = 105 / selectedGridSize;  // x grids
  var gy = k/fx;
  return gy * selectedGridSize - 68/2;
}

function init(){
  cubesGroup.selectAll('g.cube').remove();
  svg.selectAll('.lines-cls').remove();

  planeData = [[[-110/2,1,-68/2], [-110/2,1,68/2], [100/2,1,68/2], [100/2,1,-68/2]]];

  linesData = [
    [[-110/2, 1, -68/2], [-110/2, 1, 68/2]],
    [[-110/2, 1, -68/2], [100/2, 1, -68/2]],
    [[100/2, 1, -68/2], [100/2, 1, 68/2]],
    [[100/2, 1, 68/2], [-110/2, 1, 68/2]],

    [[-110/2, 1, -20/2], [-95/2, 1, -20/2]],
    [[-95/2, 1, -20/2], [-95/2, 1, 20/2]],
    [[-110/2, 1, 20/2], [-95/2, 1, 20/2]],

    [[-110/2, 1, -40/2], [-70/2,1, -40/2]],
    [[-70/2, 1, -40/2], [-70/2, 1, 40/2]],
    [[-110/2, 1, 40/2], [-70/2,1, 40/2]],

    [[-2.5, 1, -68/2], [-2.5, 1, 68/2]],

    [[100/2, 1, -20/2], [85/2, 1, -20/2]],
    [[85/2, 1, -20/2], [85/2, 1, 20/2]],
    [[100/2, 1, 20/2], [85/2, 1, 20/2]],

    [[100/2, 1, -40/2], [60/2, 1, -40/2]],
    [[60/2, 1, -40/2], [60/2, 1, 40/2]],
    [[100/2, 1, 40/2], [60/2,1, 40/2]],

  ];

  cubesData = [];

  var playerData = possessionData[selectedPlayer][selectedHalf];
  console.log(playerData);
  for(var k in playerData) {
      var h = -playerData[k]/3;
      var _cube = makeCube(h, getX(k), getZ(k));
      _cube.id = 'cube_' + k;
      _cube.height = h;
      cubesData.push(_cube);
  }

  processData(cubes3D(cubesData), plane3D(planeData), lines3D(linesData), 1000);
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

    svg.selectAll('.lines-cls').remove();

    cubeDrag = cubes3D.rotateY(beta + startAngle).rotateX(alpha - startAngle)(cubesData);
    planeDrag = plane3D.rotateY(beta + startAngle).rotateX(alpha - startAngle)(planeData);
    lineDrag = lines3D.rotateY(beta + startAngle).rotateX(alpha - startAngle)(linesData);

    processData(cubeDrag, planeDrag, lineDrag, 0);
}

function dragEnd(){
    mouseX = d3.event.x - mx + mouseX;
    mouseY = d3.event.y - my + mouseY;
}

function makeCube(h, x, z){
    return [
        {x: x - 0.4 * selectedGridSize, y: h, z: z + 0.4 * selectedGridSize}, // FRONT TOP LEFT
        {x: x - 0.4 * selectedGridSize, y: 0, z: z + 0.4 * selectedGridSize}, // FRONT BOTTOM LEFT
        {x: x + 0.4 * selectedGridSize, y: 0, z: z + 0.4 * selectedGridSize}, // FRONT BOTTOM RIGHT
        {x: x + 0.4 * selectedGridSize, y: h, z: z + 0.4 * selectedGridSize}, // FRONT TOP RIGHT
        {x: x - 0.4 * selectedGridSize, y: h, z: z - 0.4 * selectedGridSize}, // BACK  TOP LEFT
        {x: x - 0.4 * selectedGridSize, y: 0, z: z - 0.4 * selectedGridSize}, // BACK  BOTTOM LEFT
        {x: x + 0.4 * selectedGridSize, y: 0, z: z - 0.4 * selectedGridSize}, // BACK  BOTTOM RIGHT
        {x: x + 0.4 * selectedGridSize, y: h, z: z - 0.4 * selectedGridSize}, // BACK  TOP RIGHT
    ];
}

// d3.selectAll('button').on('click', init);

function loadData() {
  d3.json("../static/data/DFL-MAT-0025I9_bp_gs" + selectedGridSize + ".json", function(error, dat) {
    possessionData = dat;
    init();
  });
}

$(document).ready(function() {
  loadData();
});
