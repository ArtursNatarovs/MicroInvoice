console.log("chart function");

    let chartInstance; // Variable to hold the chart instance

    const createChart = () => {
      const ctx = document.getElementById("myChart").getContext("2d");

      // Destroy the existing chart instance if it exists
      if (chartInstance) {
        chartInstance.destroy();
      }

      // Data for the chart
      const data = {
        labels: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        datasets: [
          {
            label: "Weekly Data",
            data: [16000, 23800, 18000, 21000, 23000, 24000, 13400],
            borderColor: "blue",
            tension: 0.3, // Makes the line smooth
            fill: false, // No area below the line
          },
        ],
      };

      // Chart configuration
      const config = {
  type: "line",
  data: data,
  options: {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        display: true,
        position: "top",
        labels: {
          font: {
            size: 14, // Increase legend font size
          },
        },
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: "Days of the Week",
          font: {
            size: 16, // Larger font for the title
          },
          color: "#000", // High-contrast color
        },
        ticks: {
          font: {
            size: 14, // Larger font for labels
          },
          color: "#000", // High-contrast color
          maxRotation: 45, // Rotate labels to prevent overlap
          minRotation: 0,  // Minimum rotation angle
        },
      },
      y: {
        title: {
          display: true,
          text: "Values",
          font: {
            size: 16, // Larger font for the title
          },
          color: "#000", // High-contrast color
        },
        ticks: {
          font: {
            size: 14, // Larger font for labels
          },
          color: "#000", // High-contrast color
          stepSize: 2000, // Define clear intervals
        },
        grid: {
          drawBorder: true, // Keep borders around the Y-axis
          color: "#e0e0e0", // Subtle gridline color
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
