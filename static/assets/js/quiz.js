let intro = document.querySelector(".intro");
let logo = document.querySelector(".logoHeader");
let logoSpan = document.querySelectorAll(".logo");

window.addEventListener("DOMContentLoaded", ()=>{

    setTimeout(() => {
        logoSpan[0].classList.add("active");
    }, 1000);

    setTimeout(() => {
        logoSpan[1].classList.add("active");
        logoSpan[2].classList.add("active");
    }, 2000);


    setTimeout(() => {
        logoSpan[0].classList.remove("active");
        logoSpan[2].classList.remove("active");
        logoSpan[0].classList.add("fade");
        logoSpan[2].classList.add("fade");
        logoSpan[1].classList.add("fade");
    }, 3000);

    setTimeout(() => {
        logoSpan[1].classList.remove("active");
        
    }, 4000)

    setTimeout(() => {
        intro.style.top = "200vh";
    }, 5000)
})
    var questions = [];

    fetch('/get_questions')
      .then(response => response.json())
      .then(data => {
        questions = data.questions;
        updateQuestion(); 
      });


    var currentQuestionIndex = 0;

    function updateQuestion() {
      document.getElementById('frontFace').innerText = questions[currentQuestionIndex];
      document.getElementById('backFace').innerText = questions[(currentQuestionIndex + 1) % questions.length];
    }

    function handleCardClick(event) {
      const cardContainer = document.querySelector('.card-container');
      const card = document.querySelector('.card');

      const clickX = event.clientX - cardContainer.getBoundingClientRect().left;

      if (clickX > cardContainer.offsetWidth / 2) {
        
        currentQuestionIndex = (currentQuestionIndex + 1) % questions.length;
      } else {
        currentQuestionIndex = (currentQuestionIndex - 1 + questions.length) % questions.length;
      }

      card.classList.toggle('flip');
      setTimeout(() => {
        cardContainer.style.transform = card.classList.contains('flip') ? 'rotateY(180deg)' : 'rotateY(0deg)';
        updateQuestion();
      }, 250); 
    }
    
    updateQuestion(); 

    function addNewQuestion() {
      const userInput = document.getElementById('userInput').value.trim();
    
      if (userInput !== '') {
        fetch('/add_question', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ question: userInput }),
        })
          .then(response => response.json())
          .then(data => {
            if (data.success) {
              questions.push(userInput);
              alert('New question added successfully!');
              document.getElementById('userInput').value = ''; 
              updateQuestion();
            } else {
              alert('Failed to add question to MongoDB. Please try again.');
            }
          });
      } else {
        alert('Please enter a valid question.');
      }
    }
    
    
