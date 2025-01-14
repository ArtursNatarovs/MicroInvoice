console.log("chart function");

    let chartInstance; // Variable to hold the chart instance

    const createChart = async () => {
  const ctx = document.getElementById("myChart").getContext("2d");

  // Destroy the existing chart instance if it exists
  if (chartInstance) {
    chartInstance.destroy();
  }

  // Fetch the sales data from the backend
  const response = await fetch("/get-sales-data");
  const data = await response.json();

  // Data for the chart
  const chartData = {
    labels: data.labels, // e.g., ['2024-09', '2024-10', '2024-11', '2024-12', '2025-01']
    datasets: [
      {
        label: "Monthly Sales",
        data: data.sales, // e.g., [1000, 2000, 1500, 3000, 2500]
        backgroundColor: "rgba(54, 162, 235, 0.5)",
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 1,
      },
    ],
  };

  // Chart configuration
  const config = {
    type: "bar",
    data: chartData,
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: true,
          position: "top",
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "Months",
          },
        },
        y: {
          title: {
            display: true,
            text: "Total Sales",
          },
          ticks: {
            stepSize: 1000, // Adjust as needed
          },
        },
      },
    },
  };

  // Create the chart and store the instance
  chartInstance = new Chart(ctx, config);
};

    // Call the function to create the chart
    document.addEventListener("DOMContentLoaded", createChart);




    document.addEventListener("DOMContentLoaded", () => {
      const tableBody = document.querySelector(".table-responsive tbody");

      // Fetch data from the Flask endpoint
      fetch("/get-services")
        .then((response) => response.json())
        .then((data) => {
          // Clear existing rows
          tableBody.innerHTML = "";

          // Populate rows dynamically
          data.forEach((service, index) => {
            const row = `
              <tr>
                <td>${index + 1}</td>
                <td>${service.name}</td>
                <td>${service.price}</td>
                <td>${service.quantity}</td>
                <td>${service.total}</td>
              </tr>
            `;
            tableBody.innerHTML += row;
          });
        })
        .catch((error) => console.error("Error fetching services:", error));
    });
