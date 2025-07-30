document.addEventListener("DOMContentLoaded", () => {
  const faqForm = document.getElementById("faqForm");
  const faqInput = document.getElementById("faqInput");
  const channelSelect = document.getElementById("channelSelect");
  const faqList = document.getElementById("faqList");
  const notificationButton = document.querySelector("button.btn-outline-primary");

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

  const backendBaseUrl = 'http://127.0.0.1:5000';

  // Notification state
  let notifications = [];
  let notificationVisible = false;

  // Create notification container
  const notificationContainer = document.createElement("div");
  notificationContainer.id = "notificationContainer";
  notificationContainer.style.position = "fixed";
  notificationContainer.style.top = "60px";
  notificationContainer.style.right = "20px";
  notificationContainer.style.width = "300px";
  notificationContainer.style.maxHeight = "400px";
  notificationContainer.style.overflowY = "auto";
  notificationContainer.style.backgroundColor = "#fff";
  notificationContainer.style.border = "1px solid #ccc";
  notificationContainer.style.boxShadow = "0 2px 8px rgba(0,0,0,0.2)";
  notificationContainer.style.padding = "10px";
  notificationContainer.style.display = "none";
  notificationContainer.style.zIndex = "1000";
  document.body.appendChild(notificationContainer);

  // Toggle notification container visibility
  notificationButton.addEventListener("click", () => {
    notificationVisible = !notificationVisible;
    notificationContainer.style.display = notificationVisible ? "block" : "none";
  });

  // Add notification to container
  function addNotification(message) {
    notifications.push(message);
    const notifElement = document.createElement("div");
    notifElement.textContent = message;
    notifElement.style.borderBottom = "1px solid #ddd";
    notifElement.style.padding = "5px 0";
    notificationContainer.appendChild(notifElement);
    // Show alert as well
    alert(message);
  }

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
      fetch(`${backendBaseUrl}/faqs`, {
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
        // Add to FAQ list at the top
        const li = document.createElement("li");
        li.className = "list-group-item";
        li.innerHTML = `✅ <strong>${channel}</strong>: ${question}`;
        faqList.insertBefore(li, faqList.firstChild);

        // Update chart data
        faqCounts[channel]++;
        updateCharts();

        // Clear form
        faqInput.value = "";
        channelSelect.value = "WhatsApp";

        // Add notification
        addNotification(`New question submitted on ${channel}: "${question}"`);
      })
      .catch(error => {
        alert(error.message);
      });
    }
  });

  // Sidebar menu click effect and smooth scroll to sections
  const sidebarLinks = document.querySelectorAll(".sidebar .nav-link");
  sidebarLinks.forEach(link => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      sidebarLinks.forEach(l => l.classList.remove("active"));
      link.classList.add("active");
      const targetId = link.getAttribute("href").substring(1);
      const targetElement = document.getElementById(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({ behavior: "smooth" });
      }
    });
  });

  function updateCharts() {
    const values = Object.values(faqCounts);
    platformChart.data.datasets[0].data = values;
    faqChart.data.datasets[0].data = values;
    platformChart.update();
    faqChart.update();
  }

  function fetchFAQs() {
    fetch(`${backendBaseUrl}/faqs`)
      .then(response => response.json())
      .then(data => {
        // Sort FAQs by times_asked descending
        data.sort((a, b) => (b.times_asked || 0) - (a.times_asked || 0));
        // Clear existing FAQ list
        faqList.innerHTML = '';
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
    fetch(`${backendBaseUrl}/platforms`)
      .then(response => response.json())
      .then(data => {
        // Update platform usage counts based on active platforms
        data.forEach(platform => {
          if (platform.is_active && faqCounts.hasOwnProperty(platform.name)) {
            faqCounts[platform.name]++;
          }
        });
        updateCharts();
        console.log('Platforms:', data);
      })
      .catch(error => {
        console.error('Error fetching platforms:', error);
      });
  }

  function fetchAnalytics() {
    fetch(`${backendBaseUrl}/analytics`)
      .then(response => response.json())
      .then(data => {
        // Populate analytics summary cards with latest data
        if (data.length > 0) {
          const latest = data[data.length - 1];
          document.getElementById('totalMessages').textContent = latest.total_messages || 0;
          document.getElementById('uniqueUsers').textContent = latest.unique_users || 0;
          document.getElementById('avgResponseTime').textContent = latest.avg_response_time ? latest.avg_response_time.toFixed(2) : 0;
          document.getElementById('mostActivePlatform').textContent = latest.most_active_platform || 'N/A';
        }
        console.log('Analytics:', data);
      })
      .catch(error => {
        console.error('Error fetching analytics:', error);
      });
  }

  // Poll analytics every 10 seconds for dynamic updates
  setInterval(fetchAnalytics, 10000);
});
//chat bot functionality
document.getElementById("send-btn").addEventListener("click", async () => {
  const userInput = document.getElementById("user-input").value;
  const response = await fetch("http://localhost:5000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: userInput })
  });
  const data = await response.json();
  document.getElementById("messages").innerHTML += `
    <div><strong>You:</strong> ${userInput}</div>
    <div><strong>Bot:</strong> ${data.reply}</div>
  `;
});
