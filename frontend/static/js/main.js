document.addEventListener("DOMContentLoaded", () => {
  const faqForm = document.getElementById("faqForm");
  const faqInput = document.getElementById("faqInput");
  const channelSelect = document.getElementById("channelSelect");
  const faqList = document.getElementById("faqList");

  const faqCounts = {
    WhatsApp: 0,
    SMS: 0,
    Facebook: 0,
    Twitter: 0,
    Instagram: 0,
    TikTok: 0,
    Email: 0
  };

  const channelColors = {
    WhatsApp: "#25D366",
    SMS: "#ffc107",
    Facebook: "#3b5998",
    Twitter: "#1da1f2",
    Instagram: "#e1306c",
    TikTok: "#010101",
    Email: "#6c757d"
  };

  // Chart setup
  const platformChart = new Chart(document.getElementById("platformChart"), {
    type: "pie",
    data: {
      labels: Object.keys(faqCounts),
      datasets: [{
        label: "Platform Usage",
        data: Object.values(faqCounts),
        backgroundColor: Object.keys(faqCounts).map(c => channelColors[c])
      }]
    }
  });

  const faqChart = new Chart(document.getElementById("faqChart"), {
    type: "bar",
    data: {
      labels: Object.keys(faqCounts),
      datasets: [{
        label: "FAQs Submitted",
        data: Object.values(faqCounts),
        backgroundColor: Object.keys(faqCounts).map(c => channelColors[c])
      }]
    },
    options: {
      scales: {
        y: { beginAtZero: true }
      }
    }
  });

  // Submit handler
  faqForm.addEventListener("submit", e => {
    e.preventDefault();
    const question = faqInput.value.trim();
    const channel = channelSelect.value;

    if (question && channel) {
      // Add to FAQ list
      const li = document.createElement("li");
      li.className = "list-group-item";
      li.innerHTML = ✅ <strong>${channel}</strong>: ${question};
      faqList.appendChild(li);

      // Update chart data
      faqCounts[channel]++;
      updateCharts();

      // Clear form
      faqInput.value = "";
      channelSelect.value = "WhatsApp";
    }
  });

  function updateCharts() {
    const values = Object.values(faqCounts);
    platformChart.data.datasets[0].data = values;
    faqChart.data.datasets[0].data = values;
    platformChart.update();
    faqChart.update();
  }
});