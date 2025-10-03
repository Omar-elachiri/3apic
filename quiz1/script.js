let currentQuestion = 0;
let score = 0;
let questions = [];

fetch("questions.json")
  .then(response => response.json())
  .then(data => {
    questions = data;
    loadQuestion();
  });

function loadQuestion() {
  const quiz = document.getElementById("quiz");
  quiz.innerHTML = "";

  if (currentQuestion < questions.length) {
    const q = questions[currentQuestion];
    const questionEl = document.createElement("div");
    questionEl.className = "question";
    questionEl.innerHTML = `<h2>${q.question}</h2>`;

    const answersEl = document.createElement("div");
    answersEl.className = "answers";

    q.answers.forEach((answer, index) => {
      const btn = document.createElement("button");
      btn.textContent = answer;
      btn.onclick = () => checkAnswer(index);
      answersEl.appendChild(btn);
    });

    quiz.appendChild(questionEl);
    quiz.appendChild(answersEl);
  } else {
    showResult();
  }
}

function checkAnswer(index) {
    const q = questions[currentQuestion];
    const buttons = document.querySelectorAll(".answers button");
  
    buttons.forEach((btn, i) => {
      btn.classList.add("disabled");
      if (i === q.correct) {
        btn.classList.add("correct");
      } else if (i === index) {
        btn.classList.add("incorrect");
      }
    });
  
    if (index === q.correct) {
      score++;
    }
  
    // Attendre un peu avant de passer à la question suivante
    setTimeout(() => {
      currentQuestion++;
      loadQuestion();
    }, 1200);
  }

function showResult() {
  document.getElementById("quiz").classList.add("hidden");
  const resultEl = document.getElementById("result");
  resultEl.classList.remove("hidden");
  resultEl.textContent = `🎉 Vous avez obtenu ${score} / ${questions.length} bonnes réponses !`;
}