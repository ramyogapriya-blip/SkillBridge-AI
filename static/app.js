const form = document.getElementById("assessmentForm");
const result = document.getElementById("result");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = Object.fromEntries(new FormData(form).entries());

  result.classList.remove("hidden");
  result.innerHTML = "<p>Analyzing your profile...</p>";

  try {
    const res = await fetch("/assessment", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    result.innerHTML = `
      <div class="result-top">
        <div>
          <p class="eyebrow">AI RECOMMENDATION</p>
          <h2>${escapeHtml(data.career)}</h2>
          <p>${escapeHtml(data.recommendation)}</p>
        </div>

        <div class="score">
          ${data.readiness}%
          <small>readiness</small>
        </div>
      </div>

      <h3>Your Next Skills</h3>

      <div class="chips">
        ${data.skill_gap.map(skill =>
          `<span>${escapeHtml(skill)}</span>`
        ).join("")}
      </div>

      <a class="btn small" href="#resources">
        Explore Resources ↓
      </a>
    `;

  } catch (error) {
    result.innerHTML =
      "<p>Something went wrong. Please try again.</p>";
  }
});


function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, character => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;"
  }[character]));
}


async function loadCards() {

  const courses = await fetch("/courses")
    .then(response => response.json());

  document.getElementById("courseGrid").innerHTML =
    courses.map(course => `
      <article class="resource card">

        <span class="tag">
          ${course.type}
        </span>

        <h3>
          ${course.title}
        </h3>

        <p>
          ${course.skill} • ${course.level}
        </p>

        <a href="${course.url}"
           target="_blank"
           rel="noopener">
          Learn →
        </a>

      </article>
    `).join("");


  const jobs = await fetch("/jobs")
    .then(response => response.json());

  document.getElementById("jobGrid").innerHTML =
    jobs.map(job => `
      <article class="resource card">

        <span class="tag">
          ${job.level}
        </span>

        <h3>
          ${job.title}
        </h3>

        <p>
          ${job.skills}
        </p>

        <strong>
          ${job.location}
        </strong>

      </article>
    `).join("");
}


loadCards();
