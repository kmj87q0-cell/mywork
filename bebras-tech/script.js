//===================================================
// Bebras Technology Challenge
// script.js   Step1 전역변수 설정
//===================================================


//===================================================
// 환경 설정
//===================================================

const ROWS = 8;
const COLS = 10;


//===================================================
// HTML 객체
//===================================================

const grid =
document.getElementById("grid");

const resultMessage =
document.getElementById("resultMessage");

const runButton =
document.getElementById("runBtn");

const resetButton =
document.getElementById("resetBtn");

const submitButton =
document.getElementById("submitBtn");


//===================================================
// 게임 상태
//===================================================

const game = {

    rows: ROWS,

    cols: COLS,

    beaver:{

        row:0,

        col:0

    },

    goal:{

        row:6,

        col:8

    },

    score:0,

    currentProblem:0,

    selectedAnswer:null,

    isRunning:false

};

//===================================================
// Step2 격자 생성
//===================================================

function createGrid(){

    grid.innerHTML="";

    for(let r=0;r<game.rows;r++){

        for(let c=0;c<game.cols;c++){

            const cell=document.createElement("div");

            cell.className="cell";

            cell.dataset.row=r;

            cell.dataset.col=c;

            grid.appendChild(cell);

        }

    }

}

//===================================================
// Step3 셀 가져오기
//===================================================

function getCell(row,col){

    return document.querySelector(

`.cell[data-row="${row}"][data-col="${col}"]`

    );

}

//===================================================
// Step4 화면 그리기
//===================================================

function drawBoard(){

    document
    .querySelectorAll(".cell")
    .forEach(cell=>{

        cell.textContent="";

    });

    getCell(

        game.beaver.row,

        game.beaver.col

    ).textContent="🦫";

    getCell(

        game.goal.row,

        game.goal.col

    ).textContent="📦";

}

//===================================================
// Step5 시작
//===================================================

createGrid();

drawBoard();

