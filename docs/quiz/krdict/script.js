// LEVEL_LIST = { "8":49, ... }
// HANJA_LIST = [ { c:"校", l:"8", h:[huneums], d:[index in words] } ... ]
// import { LEVEL_LIST, HANJA_LIST } from './_data/letters.js';

// WORDS = [{ w:"가가호호1", o:"家家戶戶", c:"명", m:"meaning", e:"example" } ... ]
// import { WORDS } from './_data/words.js';

// HUNEUM = { "가":[{c:"家",h:"집"}, ...] }
// import { HUNEUM } from './_data/huneum.js'

// ***************
// Randomness func
// ***************

// random int in [start, end)
function pick_int(start, end) {
    if (end <= start + 1) {
        return start;
    }
    return Math.floor(Math.random() * (end - start)) + start;
}

// randomly choose numbers from [start, end)
// Floyd's algorithm
function pick_combination(start, end, choose) {
    let answers = [];
    for (let current_end = end - choose + 1; current_end <= end; current_end++) {
        let answer = pick_int(start, current_end);
        if (answers.includes(answer)) {
            answers.push(current_end - 1);
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

// ***************
// Initialize quiz
// ***************

// array of {
//   hanja_i: (index in hanja_list),
//   word_i: (index in words),
//   hanja_i_in_word: (index of hanja in the word),
//   sentence: (sentence to display),
//   options: [{hanja: '', huneum: ''}] * 4,
//   correct_option: (correct option = 0~3)
// }
let quizzes = [];

function initialize_quizzes(quiz_count = 20, level = '0', option_count = 4) {
    quizzes.length = 0;
    quizzes = [];

    for (let i = 0; i < quiz_count; i++) {
        // 1. pick hanja
        let hanja_i_limit = HANJA_LIST.length;
        if (level in LEVEL_LIST) {
            hanja_i_limit = LEVEL_LIST[level] + 1;
        }
        const hanja_i = pick_int(0, hanja_i_limit);
        const hanja = HANJA_LIST[hanja_i]['c'];

        // 2. pick word
        if (hanja_i >= HANJA_LIST.length) {
            console.log('Error - unexpected hanja index: ', hanja, hanja_i);
            continue;
        }
        const dict_appearances = HANJA_LIST[hanja_i]['d'];
        const word_i = dict_appearances[pick_int(0, dict_appearances.length)];
        if (word_i >= WORDS.length) {
            console.log('Error - unexpected word index: ', word, word_i);
            continue;
        }
        const word = WORDS[word_i]['w'];

        // 3. pick sentence
        const sentences = WORDS[word_i]['e'].split('\n');
        let sentence = sentences[pick_int(0, sentences.length)];
        // "Ⅱ|반장은 가가호호 찾아다니며 반상회 참여를 권유했다." 등 문장 앞 정리하기
        sentence = sentence.split('|').at(-1);

        // 4. create options
        // 4-1. get correct eum
        const original = WORDS[word_i]['o'];
        const hanja_i_in_word = original.indexOf(hanja);
        if (hanja_i_in_word < 0) {
            console.log('Error - hanja not in word: ', hanja, word, original);
            continue;
        }
        if (hanja_i_in_word >= word.length) {
            console.log('Error - word and original word in dictionary do not match: ', word, original);
            continue;
        }
        let eum = word[hanja_i_in_word];
        let hun = ''
        // exception: 음이 달라진 한자 (ex: 사탕 = 沙糖▽)
        let eum_changed = true;
        for (let huneum of HANJA_LIST[hanja_i]['h']) {
            if (huneum.at(-1) === eum) {
                eum_changed = false;
                hun = huneum.slice(0, -2);
                break;
            }
        }
        if (eum_changed) { // 그냥 훈음 목록의 첫 음으로 하기
            const huneum = HANJA_LIST[hanja_i]['h'][0]
            eum = huneum.at(-1);
            hun = huneum.slice(0, -2);
        }

        // 4-2. get list of hun
        const hun_count = HUNEUM[eum].length
        let hun_index;
        for (hun_index = 0; hun_index < hun_count; hun_index++) {
            if (HUNEUM[eum][hun_index]['h'] === hun) break;
        }
        if (hun_index >= hun_count) {
            console.log('Error - could not find hun: ', hanja, hun);
            continue;
        }

        // 4-3. select other three options
        let options = [];
        
        // if number of hun is more than number of options: randomly select other three
        if (hun_count > option_count) {

            let option_indexes = [];

            // pick (option_count - 1) wrong options from [0, hun_count - 1)
            // then add 1 for each number >= hun_index
            // TODO: add filter to only use hanjas up to a certain difficulty level
            option_indexes = pick_combination(0, hun_count - 1, option_count - 1)
                .map((index) => (index >= hun_index ? index + 1 : index));
            
            // create {hanja: '', huneum: ''} pairs
            options = option_indexes.map((index) => {
                if (index >= HUNEUM[eum].length) {
                    console.log('Error', HUNEUM[eum], index, hun_index, option_indexes);
                }
                let option_hanjas = HUNEUM[eum][index]['c'];
                let option_hanja = option_hanjas[pick_int(0, option_hanjas.length)];
                return {
                    'hanja': option_hanja,
                    'huneum': HUNEUM[eum][index]['h'] + ' ' + eum
                };
            });
            // add correct option
            options.push({
                'hanja': hanja,
                'huneum': hun + ' ' + eum
            });
        } else {
            // put in all the huns
            options = HUNEUM[eum].map((option_object) => {
                let option_hanjas = option_object['c'];
                let option_hun = option_object['h'];

                let option_hanja = '';
                if (option_hun === hun) {
                    option_hanja = hanja;
                } else {
                    option_hanja = option_hanjas[pick_int(0, option_hanjas.length)];
                }

                return {
                    'hanja': option_hanja,
                    'huneum': option_hun + ' ' + eum
                };
            });

            // add dummy
            // TODO: add dummy hun from the list of all huneum
            while (options.length < option_count) {
                options.push({
                    'hanja': '',
                    'huneum': '(다른 한자 없음)'
                });
            }
        }

        // 5. shuffle and choose correct_option
        shuffle(options);
        let correct_option;
        for (correct_option = 0; correct_option < options.length; correct_option++) {
            if (options[correct_option]['hanja'] === hanja) {
                break;
            }
        }
        if (correct_option >= options.length) {
            console.log('Error - hanja went missing while creating options');
            console.log(options);
            continue;
        }

        quizzes.push({
            hanja_i, word_i, hanja_i_in_word, sentence, options, correct_option
        });
    }
}


// ************
// Display quiz
// ************

const E_quiz_word = document.querySelector('.quiz-word');
const E_quiz_sentence = document.querySelector('.quiz-sentence');
const E_quiz_meaning = document.querySelector('.quiz-meaning');
const E_quiz_flavor = document.querySelector('.quiz-flavor');
const EL_quiz_btns = document.querySelectorAll('.quiz-btns button');
const E_quiz_btn_next = document.querySelector('.quiz-btn-next button');

let quiz_index = 0;

function display_quiz() {
    if (quiz_index >= quizzes.length) {
        return;
    }
    const quiz = quizzes[quiz_index];

    // 1. set word
    let word_array = WORDS[quiz.word_i]['w'].split('');

    E_quiz_word.innerHTML = word_array.map((char, i) => (
        (char >= '0' && char <= '9') ? '' : // 표제어 뒤의 동형어 번호 지우기
        (i === quiz.hanja_i_in_word) ? '<b>' + char + '</b>' : char // 맞출 글자 강조하기
    )).join('');

    // 2. set sentence and flavor
    const sentence_split = quiz.sentence.split('≪');
    let sentence = sentence_split[0];
    let flavor = '';
    if (sentence_split.length > 1) {
        flavor = sentence_split.at(-1);
    }
    E_quiz_sentence.innerHTML = '&ldquo;' + sentence + '&rdquo;';
    E_quiz_flavor.innerHTML = flavor;

    // 3. remove meaning
    E_quiz_meaning.innerHTML = '';

    // 3. set options
    for (let i=0; i < EL_quiz_btns.length; i++) {
        EL_quiz_btns[i].innerHTML = quiz.options[i].huneum;
    }

    // 4. set class for correct button
    for (let E_btn of EL_quiz_btns) {
        E_btn.classList.remove('correct');
        E_btn.classList.remove('selected');
        E_btn.disabled = false;
    }
    EL_quiz_btns[quiz.correct_option].classList.add('correct');

    // 5. hide UI
    E_quiz_btn_next.hidden = true;
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

function display_quiz_answer() {
    if (quiz_index >= quizzes.length) {
        return;
    }
    const quiz = quizzes[quiz_index];

    // 1. set word
    let word = WORDS[quiz.word_i]['w'];
    word = word.replaceAll(/\d/g, '');
    let original = WORDS[quiz.word_i]['o'];
    
    // "<ruby>登<rt>등</rt></ruby><ruby>校<rt>교</rt></ruby>하다" 꼴로 만들기
    const word_innerHTML_list = [];
    for (let i=0; i<word.length; i++) {
        if (word[i] === original[i]) {
            word_innerHTML_list.push(word[i]);
        } else {
            word_innerHTML_list.push(
                '<ruby>' + original[i] + '<rt>' + word[i] + '</rt></ruby>'
            );
        }
    }
    E_quiz_word.innerHTML = word_innerHTML_list.join('');

    // 2. set word meaning
    E_quiz_meaning.innerHTML = WORDS[quiz.word_i]['m'];

    // 3. set options
    for (let i=0; i < EL_quiz_btns.length; i++) {
        if (quiz.options[i].hanja !== '') {
            EL_quiz_btns[i].innerHTML =  quiz.options[i].huneum + '&nbsp;(' + quiz.options[i].hanja + ')';
        }
    }

    // 4. display UI
    E_quiz_btn_next.hidden = false;

    add_onclick();
}


// *************************
// Adding onclick to buttons
// *************************

for (let E_btn of EL_quiz_btns) {
    E_btn.addEventListener('click', (e) => {
        // 1. disable buttons
        for (let E_btn of EL_quiz_btns) {
            E_btn.disabled = true;
        }

        // if 'selected' button is not 'correct', it will turn red
        e.target.classList.add('selected');

        // 2. display answer
        display_quiz_answer();
    });
}

E_quiz_btn_next.addEventListener('click', (e) => {
    quiz_index += 1;
    if (quiz_index < quizzes.length) {
        display_quiz();
    } else {
        initialize_quizzes();
        quiz_index = 0;
        display_quiz();
    }
    
});

initialize_quizzes();
display_quiz();