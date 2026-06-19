console.log("dashboard.js loaded");

let sdgChartInstance = null;
let confidenceBySdgChartInstance = null;
let keywordsChartInstance = null;

let activeFilters = {
    sdg: null,
    minConf: 0
};

function buildQueryParams() {
    const params = new URLSearchParams();

    if (activeFilters.sdg) params.append("sdg", activeFilters.sdg);
    if (activeFilters.minConf !== null) params.append("min_conf", activeFilters.minConf);

    return params.toString();
}

async function fetchJSON(url) {
    const response = await fetch(url);

    if (!response.ok) {
        const text = await response.text();
        throw new Error(`Request failed -> ${url} -> ${response.status} -> ${text}`);
    }

    return await response.json();
}

function updateActiveSdgBadge() {
    const badge = document.getElementById("activeSdgBadge");
    if (!badge) return;
    badge.textContent = activeFilters.sdg ? activeFilters.sdg : "All SDGs";
}

function getBarColors(labels) {
    return labels.map(label => {
        if (!activeFilters.sdg) return "rgba(31, 111, 235, 0.85)";
        return label === activeFilters.sdg
            ? "rgba(77, 163, 255, 1)"
            : "rgba(255,255,255,0.18)";
    });
}

async function loadFilterOptions() {
    const data = await fetchJSON("/api/filter-options");
    const sdgSelect = document.getElementById("sdgFilter");

    sdgSelect.innerHTML = `<option value="">All SDGs</option>`;

    (data.sdgs || []).forEach(sdg => {
        const option = document.createElement("option");
        option.value = sdg;
        option.textContent = sdg;
        sdgSelect.appendChild(option);
    });
}

async function loadSummary() {
    const data = await fetchJSON(`/api/summary?${buildQueryParams()}`);

    document.getElementById("kpiTotalArticles").textContent = data.total_articles ?? 0;
    document.getElementById("kpiAvgConfidence").textContent = `${data.avg_confidence ?? 0}%`;
    document.getElementById("kpiTopSdg").textContent = data.top_sdg ?? "N/A";
    document.getElementById("kpiAvgWordCount").textContent = data.avg_word_count ?? 0;
}

async function loadSdgDistribution() {
    const data = await fetchJSON(`/api/sdg-distribution?${buildQueryParams()}`);
    const canvas = document.getElementById("sdgDistributionChart");
    const ctx = canvas.getContext("2d");

    if (sdgChartInstance) sdgChartInstance.destroy();

    sdgChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: data.labels || [],
            datasets: [{
                label: "Articles per SDG",
                data: data.values || [],
                backgroundColor: getBarColors(data.labels || []),
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            onClick: (evt, elements) => {
                if (!elements.length) return;

                const index = elements[0].index;
                const clickedSdg = data.labels[index];

                activeFilters.sdg = activeFilters.sdg === clickedSdg ? null : clickedSdg;
                document.getElementById("sdgFilter").value = activeFilters.sdg || "";
                updateAll();
            },
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    ticks: { color: "#d6dae0" },
                    grid: { color: "rgba(255,255,255,0.05)" }
                },
                y: {
                    ticks: { color: "#d6dae0" },
                    grid: { color: "rgba(255,255,255,0.05)" }
                }
            }
        }
    });
}

async function loadConfidenceBySdg() {
    const data = await fetchJSON(`/api/confidence-by-sdg?${buildQueryParams()}`);
    const canvas = document.getElementById("confidenceBySdgChart");
    const ctx = canvas.getContext("2d");

    if (confidenceBySdgChartInstance) confidenceBySdgChartInstance.destroy();

    confidenceBySdgChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: data.labels || [],
            datasets: [{
                label: "Average Confidence",
                data: data.values || [],
                backgroundColor: getBarColors(data.labels || [])
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    ticks: { color: "#d6dae0" },
                    grid: { color: "rgba(255,255,255,0.05)" }
                },
                y: {
                    ticks: { color: "#d6dae0" },
                    grid: { color: "rgba(255,255,255,0.05)" },
                    min: 0,
                    max: 1
                }
            }
        }
    });
}

async function loadScatter() {
    const data = await fetchJSON(`/api/scatter?${buildQueryParams()}`);

    if (!data.x.length) {
        Plotly.react("scatterChart", [], {
            paper_bgcolor: "rgba(0,0,0,0)",
            plot_bgcolor: "rgba(0,0,0,0)",
            font: { color: "#d6dae0" },
            annotations: [{
                text: "No scatter data available",
                xref: "paper",
                yref: "paper",
                x: 0.5,
                y: 0.5,
                showarrow: false,
                font: { size: 16, color: "#d6dae0" }
            }]
        }, { responsive: true });
        return;
    }

    Plotly.react("scatterChart", [{
        x: data.x,
        y: data.y,
        mode: "markers",
        type: "scatter",
        text: data.titles || [],
        marker: {
            size: 7,
            color: "#3fa8ff",
            opacity: 0.65
        }
    }], {
        xaxis: {
            title: "Word Count",
            color: "#d6dae0",
            gridcolor: "rgba(255,255,255,0.06)"
        },
        yaxis: {
            title: "Top 1 Confidence",
            color: "#d6dae0",
            gridcolor: "rgba(255,255,255,0.06)"
        },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        font: { color: "#d6dae0" },
        margin: { t: 20, r: 20, b: 60, l: 60 }
    }, { responsive: true });
}

async function loadTopKeywords() {
    const data = await fetchJSON(`/api/top-keywords?${buildQueryParams()}`);
    const canvas = document.getElementById("keywordsChart");
    const ctx = canvas.getContext("2d");

    if (keywordsChartInstance) keywordsChartInstance.destroy();

    keywordsChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: data.labels || [],
            datasets: [{
                label: "Keyword Frequency",
                data: data.values || [],
                backgroundColor: "rgba(77, 163, 255, 0.82)",
                borderRadius: 8
            }]
        },
        options: {
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    ticks: { color: "#d6dae0" },
                    grid: { color: "rgba(255,255,255,0.05)" }
                },
                y: {
                    ticks: { color: "#d6dae0" },
                    grid: { display: false }
                }
            }
        }
    });
}

async function loadArticlesTable() {
    const rows = await fetchJSON(`/api/articles?${buildQueryParams()}`);
    const tbody = document.getElementById("articlesTableBody");

    tbody.innerHTML = "";

    if (!rows.length) {
        const tr = document.createElement("tr");
        tr.innerHTML = `<td colspan="6">No data available</td>`;
        tbody.appendChild(tr);
        return;
    }

    rows.forEach(row => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${row.title || ""}</td>
            <td>${row.primary_sdg || ""}</td>
            <td>${row.top1_conf ?? ""}</td>
            <td>${row.top2_sdg || ""}</td>
            <td>${row.top2_conf ?? ""}</td>
            <td>${row.word_count ?? ""}</td>
        `;
        tbody.appendChild(tr);
    });
}

async function updateAll() {
    updateActiveSdgBadge();

    await Promise.all([
        loadSummary(),
        loadSdgDistribution(),
        loadConfidenceBySdg(),
        loadScatter(),
        loadTopKeywords(),
        loadArticlesTable()
    ]);
}

let filterTimer;

function wireFilters() {
    const sdgFilter = document.getElementById("sdgFilter");
    const minConfFilter = document.getElementById("minConfFilter");
    const minConfValue = document.getElementById("minConfValue");
    const resetBtn = document.getElementById("resetFiltersBtn");

    sdgFilter.addEventListener("change", () => {
        activeFilters.sdg = sdgFilter.value || null;
        updateAll();
    });

    minConfFilter.addEventListener("input", () => {
        activeFilters.minConf = parseFloat(minConfFilter.value);
        minConfValue.textContent = activeFilters.minConf.toFixed(2);

        clearTimeout(filterTimer);
        filterTimer = setTimeout(() => {
            updateAll();
        }, 300);
    });

    resetBtn.addEventListener("click", () => {
        activeFilters = {
            sdg: null,
            minConf: 0
        };

        sdgFilter.value = "";
        minConfFilter.value = 0;
        minConfValue.textContent = "0.00";

        updateAll();
    });
}

document.addEventListener("DOMContentLoaded", async () => {
    try {
        console.log("Step 1: loadFilterOptions");
        await loadFilterOptions();

        console.log("Step 2: wireFilters");
        wireFilters();

        console.log("Step 3: updateAll");
        await updateAll();

        console.log("Dashboard initialized successfully");
    } catch (error) {
        console.error("Dashboard init failed:", error?.message || error);
        console.error("Full error object:", error);
        alert("Dashboard failed to initialize. Check Console.");
    }
});

async function loadSentimentChart() {

    const response = await fetch("/api/sentiment-distribution");

    const data = await response.json();

    const ctx = document
        .getElementById("sentimentChart")
        .getContext("2d");

    new Chart(ctx, {

        type: "doughnut",

        data: {

            labels: data.labels,

            datasets: [{

                data: data.values,

                backgroundColor: [
                    "#A21942",   // Negative
                    "#3F7E44",   // Positive
                    "#e6dace"    // Neutral
                ],

                borderWidth: 0,

                hoverOffset: 12,

                cutout: "28%"
            }]
        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            animation: {
                animateRotate: true,
                duration: 1800
            },

            plugins: {

                legend: {

                    position: "top",

                    labels: {

                        color: "#e7edf7",

                        padding: 18,

                        usePointStyle: true,

                        pointStyle: "circle",

                        font: {
                            size: 13,
                            weight: "600"
                        }
                    }
                },

                tooltip: {

                    backgroundColor: "#111827",

                    borderColor: "rgba(255,255,255,0.08)",

                    borderWidth: 1,

                    titleColor: "#ffffff",

                    bodyColor: "#d7dde7",

                    padding: 12,

                    displayColors: true
                }
            }
        }
    });
}

loadSentimentChart();