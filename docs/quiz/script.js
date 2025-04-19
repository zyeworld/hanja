// random int in [start, end)
function pick_int(start, end) {
    return Math.floor(Math.random() * (end - start) + start);
}

// randomly choose numbers from [start, end)
// Floyd's algorithm
function pick_combination(start, end, choose) {
    let answers = [];
    for (let current_end = end - choose + 1; current_end <= end; current_end++) {
        let answer = pick_int(start, current_end);
        if (answers.includes(answer)) {
            answers.push(current_end);
        } else {
            answers.push(answer);
        }
    }
    return answers;
}

// shuffles an array
function shuffle(arr) {
    for (let i = arr.length - 1; i >= 1; i--) {
        let j = pick_int(0, i + 1);
        let temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}

// adding onclick to all 'ruby' elements
function add_onclick() {
    const EL_ruby = document.getElementsByTagName('ruby');
    for (const E_ruby of EL_ruby) {
        E_ruby.onclick = ((e) => {
            console.log(E_ruby.innerText[0]);
        });
    }
}
add_onclick()

// quiz 1: show sentence, guess hanja
const E_quiz1 = document.getElementById('quiz1');
const E_quiz1_h1 = document.getElementById('quiz1-h1');
const E_quiz1_flavor = document.getElementById('quiz1-flavor');
const EL_quiz1_btns = E_quiz1.getElementsByTagName('button');

let quiz1_data = {
    sentence: 'asdfasdf',
    pronunciation: 'sdfgsdfg',
    source: '',
    main_letters: '',
    main_level: '',
    mistakable_for: ''
};

let quiz1_options = [
    { hanja: '', huneums: [], huneum_index: -1},
    { hanja: '', huneums: [], huneum_index: -1},
    { hanja: '', huneums: [], huneum_index: -1},
    { hanja: '', huneums: [], huneum_index: -1}
];

// 0 ~ 3
let quiz1_correct_answer = 0;

// sentence_obj: 
function set_quiz1() {
    // 1. write pronunciation to E_quiz1_h1
    if (quiz1_data.pronunciation === '') {
        quiz1_data.pronunciation = quiz1_data.sentence;
    }
    E_quiz1_h1.innerHTML = quiz1_data.pronunciation;

    // 2. create 4 options
    let answer_options = ['1', '2', '3', '4'];
    quiz1_correct_answer = 0;

    // 3. write options to EL_quiz1_btns
    for (let i = 0; i < 4; i++) {
        EL_quiz1_btns[i].innerHTML = answer_options[i];
    }
}

set_quiz1();

function set_quiz1_answer() {
    
}
