// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
  // Join Now button functionality
  const joinButton = document.querySelector("#getstarted1 button");
  if (joinButton) {
    joinButton.addEventListener("click", function () {
      console.log("Join Now button clicked");
      window.location.href = "login.html";
    });

    joinButton.addEventListener("mouseover", function () {
      this.style.transform = "scale(1.1)";
      this.style.transition = "transform 0.3s ease";
    });

    joinButton.addEventListener("mouseout", function () {
      this.style.transform = "scale(1)";
    });
  } else {
    console.error("Join Now button not found");
  }
});
// Smooth scrolling for navigation
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    document.querySelector(this.getAttribute("href")).scrollIntoView({
      behavior: "smooth",
    });
  });
});

// Simple animation for "Join Now" button
const joinButton = document.querySelector("#getstarted1 button");
joinButton.addEventListener("mouseover", () => {
  joinButton.style.transform = "scale(1.1)";
  joinButton.style.transition = "transform 0.3s ease";
});
joinButton.addEventListener("mouseout", () => {
  joinButton.style.transform = "scale(1)";
});

// Toggle functionality for FAQ questions
const questions = document.querySelectorAll(".question");
questions.forEach((question) => {
  question.addEventListener("click", () => {
    const answer = question.nextElementSibling;
    answer.style.display = answer.style.display === "none" ? "block" : "none";
  });
});

// Form submission handling for newsletter
const newsletterForm = document.querySelector(".container3 form");
newsletterForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const email = newsletterForm.querySelector('input[type="email"]').value;
  alert(`Thank you for subscribing with email: ${email}`);
  newsletterForm.reset();
});

// Animated counter for stats
function animateValue(obj, start, end, duration) {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    obj.innerHTML = Math.floor(progress * (end - start) + start);
    if (progress < 1) {
      window.requestAnimationFrame(step);
    }
  };
  window.requestAnimationFrame(step);
}

const techEnthusiasts = document.querySelector(".item2 h2");
const projects = document.querySelectorAll(".item2 h2")[1];

animateValue(techEnthusiasts, 0, 10000, 2000);
animateValue(projects, 0, 5000, 2000);
