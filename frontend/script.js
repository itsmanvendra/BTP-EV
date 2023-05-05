// const grid = document.querySelector('.grid');

// // create cells and add to grid
// for (let i = 1; i <= 10; i++) {
//   for (let j = 1; j <= 10; j++) {
//     const cell = document.createElement('div');
//     // for(let k = 1; k <= 10; k++){
//     //     for(let l = 1; l <= 10; l++){
//     //         const smallCell = document.createElement('div');
//     //         smallCell.classList.add('smallCell');
//     //         smallCell.setAttribute('data-x',i*10+k);
//     //         smallCell.setAttribute('data-y', j*10+l);
//     //         cell.appendChild(smallCell);
//     //     }
//     // }
//     cell.classList.add('cell');
//     cell.setAttribute('data-x', i);
//     cell.setAttribute('data-y', j);
//     grid.appendChild(cell);
//   }
// }

// // mark coordinates


// // Generate the grid
// for (let i = 0; i < 10; i++) {
// 	for (let j = 0; j < 10; j++) {
// 		const cell = document.createElement('div');
// 		cell.classList.add('cell');
// 		for (let k = 0; k < 10; k++) {
// 			const innerCell = document.createElement('div');
// 			innerCell.classList.add('inner-cell');
// 			cell.appendChild(innerCell);
// 		}
// 		container.appendChild(cell);
// 	}
// }
const board = document.querySelector('.board');
const cellsToHighlight = [1, 3, 5, 7, 9, 21, 23, 25, 27, 29, 41, 43, 45, 47, 49,61,63,65,67,69,81,83,85,87,89];
const sourceLocation = document.getElementById('userLocation');
const getCs = document.querySelector('.findCS');
const destination = document.getElementById('userDestination');
const soc = document.getElementById('userSoc');

const batteryCapacity = document.getElementById('userBatteryCapacity');
const ecr = document.getElementById('userEnergyConsumptionRate');
const time = document.getElementById('userTime');
// Generate the Sudoku board
// for (let i = 9; i >=0; i--) {
// 	for (let j = 0; j < 10; j++) {
// 		const cell = document.createElement('div');
// 		cell.classList.add('cell');
//         // console.log(i*9+j+i);
//         // cell.textContent(i*9+j+i);
//         cell.setAttribute('data-xd', i*9 + j+i);
		
//         // if(cellsToHighlight.includes((i-1) * 10 + j)) {
//         //     cell.classList.add('highlights');
//         // }
// 		board.appendChild(cell);
// 	}
// }

let canvas = document.getElementById("canvas");
let context = canvas.getContext("2d");
// <!--context.beginPath();-->
// <!--context.moveTo(10,0);-->
// <!--context.lineTo(10,150);-->

function initGrid(){
    clearCanvas();
    // canvas.style.backgroundColor = "#2b2b2b";
    for(let i = 1; i<=10; i++){
  context.beginPath();
  const xd = i*60;
  context.moveTo(`${xd}`, 0);
  context.lineTo(`${xd}`, 600);
  context.strokeStyle = '#fff';
  context.stroke();
  for(let j = 1; j<=5; j++){
    context.beginPath();
    const xdd =(xd-60) + j*12;
    context.moveTo(`${xdd}`, 0);
    context.lineTo(`${xdd}`, 600);
    context.strokeStyle = '#ffffff33';
    context.stroke();
  }
  context.moveTo(0, `${xd}`);
  context.lineTo(600, `${xd}`);
  context.strokeStyle = '#fff';
  context.stroke();
  for(let j = 1; j<=5; j++){
    context.beginPath();
    const xdd =(xd-60) + j*12;
    context.moveTo(0, `${xdd}`);
    context.lineTo(600, `${xdd}`);
    context.strokeStyle = '#ffffff33';
    context.stroke();
  }
  
    
}
}


function convertCoordsIntoInt(coOrd){
    let coords = coOrd;
    let coordsX;
    let coordsY;
    let xD = '';
    for(let i = 1; i<coords.length; i++){
        if(coords[i] === ','){
            coordsX = xD;
            xD = '';
        }
        else if(coords[i] === ')'){
            coordsY = xD;
            xD = '';
        }
        else{
            xD += coords[i];
        }

    }
    let coords1X = Number(coordsX);
    let coords1Y = Number(coordsY);
    let coordinates = [coords1X, coords1Y];
    return coordinates;
    

}

function highlightSourceCoords(x,y){
    context.beginPath();
    context.arc((x*60), ((10-y)*60), 10, 0, 2 * Math.PI, false);
    context.fillStyle = '#ff000080';
    context.fill();
    context.strokeStyle = 'white';
    context.stroke();
}
function highlightDestinationCoords(x,y){
    context.beginPath();
    context.arc((x*60), ((10-y)*60), 10, 0, 2 * Math.PI, false);
    context.fillStyle = '#007bff80';
    context.fill();
    context.strokeStyle = 'white';
    context.stroke();
}


function highlightCSAlloted(x,y){
    
    context.fillStyle = '#00ff79';
    context.fillRect((x*60)-20, ((10-y)*60)-20, 40, 40);
    a = true;
    
    console.log(x,y)
}

    function clearCanvas() {
        context.clearRect(0, 0, canvas.width, canvas.height);
}









initGrid();
getCs.addEventListener('click', function(e){
    e.preventDefault();
    initGrid();
    const sourceCoordinates = convertCoordsIntoInt(sourceLocation.value);
    const destinationCoordinates = convertCoordsIntoInt(destination.value);
    console.log(sourceCoordinates);
    console.log(destinationCoordinates);
    // let highlightsSCoords = (sourceCoordinates[1])*10 + (sourceCoordinates[0]);
    // let highlightsDCoords = (destinationCoordinates[1])*10 + (destinationCoordinates[0]);
    highlightSourceCoords(sourceCoordinates[0], sourceCoordinates[1]);
    highlightDestinationCoords(destinationCoordinates[0], destinationCoordinates[1]);
    // highlightsSCoords = 81-highlightsSCoords;
    // const mark1 = board.querySelector(`[data-xd="${highlightsSCoords}"]`);
    // mark1.classList.add('mark');
    // mark1.textContent = 'S';
    // const mark2 = board.querySelector(`[data-xd="${highlightsDCoords}"]`);
    // mark2.classList.add('dest');
    // mark2.textContent = 'D';

    fetch("https://hammerhead-app-895jk.ondigitalocean.app/api/findCS", {
        method: "POST",
        body: JSON.stringify({
            reqX : sourceCoordinates[0]*1000,
            reqY : sourceCoordinates[1]*1000,
            desX : destinationCoordinates[0]*1000,
            desY : destinationCoordinates[1]*1000,
            soc : Number(soc.value),
            capacity: Number(batteryCapacity.value),
            ecrUser : Number(ecr.value),

            reqTime : Number(time.value),
        }),
        headers: {
        "Content-type": "application/json"
        }
    })
    .then((response) => response.json())
    .then((json) => highlightCSAlloted((json.ans[0]/1000), (json.ans[1]/1000)))
    .catch((err) =>console.error(err));
})


