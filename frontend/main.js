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

  // Fetch initial data from backend
  fetchFAQs();
  fetchPlatforms();
  fetchAnalytics();

  // Submit handler
  faqForm.addEventListener("submit", e => {
    e.preventDefault();
    const question = faqInput.value.trim();
    const channel = channelSelect.value;

    if (question && channel) {
      // POST new FAQ to backend
      fetch('/faqs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question, category: channel })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to add FAQ');
        }
        return response.json();
      })
      .then(data => {
        // Add to FAQ list
        const li = document.createElement("li");
        li.className = "list-group-item";
        li.innerHTML = `✅ <strong>${channel}</strong>: ${question}`;
        faqList.appendChild(li);

        // Update chart data
        faqCounts[channel]++;
        updateCharts();

        // Clear form
        faqInput.value = "";
        channelSelect.value = "WhatsApp";
      })
      .catch(error => {
        alert(error.message);
      });
    }
  });

  function updateCharts() {
    const values = Object.values(faqCounts);
    platformChart.data.datasets[0].data = values;
    faqChart.data.datasets[0].data = values;
    platformChart.update();
    faqChart.update();
  }

  function fetchFAQs() {
    fetch('/faqs')
      .then(response => response.json())
      .then(data => {
        data.forEach(faq => {
          const li = document.createElement("li");
          li.className = "list-group-item";
          li.innerHTML = `✅ <strong>${faq.category}</strong>: ${faq.question}`;
          faqList.appendChild(li);
          if (faq.category && faqCounts.hasOwnProperty(faq.category)) {
            faqCounts[faq.category]++;
          }
        });
        updateCharts();
      })
      .catch(error => {
        console.error('Error fetching FAQs:', error);
      });
  }

  function fetchPlatforms() {
    fetch('/platforms')
      .then(response => response.json())
      .then(data => {
        // Optionally handle platform data if needed
        console.log('Platforms:', data);
      })
      .catch(error => {
        console.error('Error fetching platforms:', error);
      });
  }

  function fetchAnalytics() {
    fetch('/analytics')
      .then(response => response.json())
      .then(data => {
        // Optionally handle analytics data if needed
        console.log('Analytics:', data);
      })
      .catch(error => {
        console.error('Error fetching analytics:', error);
      });
  }
});
