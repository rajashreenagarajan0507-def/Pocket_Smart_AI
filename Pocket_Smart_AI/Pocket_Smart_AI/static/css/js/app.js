// ============================================================
// PocketSmart AI - Frontend JavaScript
// ============================================================

document.addEventListener("DOMContentLoaded", () => {
    initializeNavigation();
    initializeForms();
    initializeFileUpload();
});


// ============================================================
// NAVIGATION
// ============================================================

function initializeNavigation() {
    const menuButton = document.querySelector(".menu-toggle");
    const navigation = document.querySelector(".nav-links");

    if (menuButton && navigation) {
        menuButton.addEventListener("click", () => {
            navigation.classList.toggle("active");
        });
    }
}


// ============================================================
// FORM INITIALIZATION
// ============================================================

function initializeForms() {
    const homeForm = document.getElementById("homeForm");
    const partyForm = document.getElementById("partyForm");
    const jewelryForm = document.getElementById("jewelryForm");

    if (homeForm) {
        homeForm.addEventListener("submit", handleHomeSubmit);
    }

    if (partyForm) {
        partyForm.addEventListener("submit", handlePartySubmit);
    }

    if (jewelryForm) {
        jewelryForm.addEventListener("submit", handleJewelrySubmit);
    }
}


// ============================================================
// HOME PLANNER
// ============================================================

async function handleHomeSubmit(event) {
    event.preventDefault();

    const form = event.target;
    const button = form.querySelector("button[type='submit']");

    const data = {
        budget: Number(document.getElementById("homeBudget")?.value || 0),
        room_type: document.getElementById("roomType")?.value || "",
        style: document.getElementById("homeStyle")?.value || "",
        items: getHomeItems()
    };

    if (data.budget <= 0) {
        showMessage("Please enter a valid budget.", "error");
        return;
    }

    if (!data.room_type) {
        showMessage("Please select a room type.", "error");
        return;
    }

    setLoading(button, true);

    try {
        const response = await fetch("/api/generate-home", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Unable to generate recommendations.");
        }

        displayRecommendations(result);

    } catch (error) {
        console.error("Home planner error:", error);
        showMessage(error.message, "error");

    } finally {
        setLoading(button, false);
    }
}


// ============================================================
// GET HOME ITEMS
// ============================================================

function getHomeItems() {
    const items = [];

    const itemRows = document.querySelectorAll(".home-item");

    itemRows.forEach(row => {
        const nameInput = row.querySelector(".item-name");
        const quantityInput = row.querySelector(".item-quantity");

        if (nameInput && nameInput.value.trim()) {
            items.push({
                name: nameInput.value.trim(),
                quantity: Number(quantityInput?.value || 1)
            });
        }
    });

    return items;
}


// ============================================================
// PARTY PLANNER
// ============================================================

async function handlePartySubmit(event) {
    event.preventDefault();

    const form = event.target;
    const button = form.querySelector("button[type='submit']");

    const data = {
        budget: Number(document.getElementById("partyBudget")?.value || 0),
        guests: Number(document.getElementById("guests")?.value || 0),
        event_type: document.getElementById("eventType")?.value || "",
        venue: document.getElementById("venue")?.value || "",
        food_preference:
            document.getElementById("foodPreference")?.value || "",
        decoration_style:
            document.getElementById("decorationStyle")?.value || ""
    };

    if (data.budget <= 0) {
        showMessage("Please enter a valid budget.", "error");
        return;
    }

    if (data.guests <= 0) {
        showMessage("Please enter the number of guests.", "error");
        return;
    }

    if (!data.event_type) {
        showMessage("Please select an event type.", "error");
        return;
    }

    setLoading(button, true);

    try {
        const response = await fetch("/api/generate-party", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Unable to generate recommendations.");
        }

        displayRecommendations(result);

    } catch (error) {
        console.error("Party planner error:", error);
        showMessage(error.message, "error");

    } finally {
        setLoading(button, false);
    }
}


// ============================================================
// JEWELRY PLANNER
// ============================================================

async function handleJewelrySubmit(event) {
    event.preventDefault();

    const form = event.target;
    const button = form.querySelector("button[type='submit']");

    const data = new FormData();

    const budget =
        document.getElementById("jewelryBudget")?.value || "";

    const occasion =
        document.getElementById("occasion")?.value || "";

    const style =
        document.getElementById("jewelryStyle")?.value || "";

    const metal =
        document.getElementById("metalPreference")?.value || "";

    const outfitColor =
        document.getElementById("outfitColor")?.value || "";

    data.append("budget", budget);
    data.append("occasion", occasion);
    data.append("style", style);
    data.append("metal_preference", metal);
    data.append("outfit_color", outfitColor);

    const imageInput = document.getElementById("outfitImage");

    if (imageInput && imageInput.files.length > 0) {
        data.append("image", imageInput.files[0]);
    }

    if (!budget || Number(budget) <= 0) {
        showMessage("Please enter a valid budget.", "error");
        return;
    }

    if (!occasion) {
        showMessage("Please select an occasion.", "error");
        return;
    }

    setLoading(button, true);

    try {
        const response = await fetch("/api/generate-jewelry", {
            method: "POST",
            body: data
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Unable to generate recommendations.");
        }

        displayRecommendations(result);

    } catch (error) {
        console.error("Jewelry planner error:", error);
        showMessage(error.message, "error");

    } finally {
        setLoading(button, false);
    }
}


// ============================================================
// FILE UPLOAD PREVIEW
// ============================================================

function initializeFileUpload() {
    const imageInput = document.getElementById("outfitImage");
    const preview = document.getElementById("imagePreview");

    if (!imageInput) {
        return;
    }

    imageInput.addEventListener("change", () => {
        const file = imageInput.files[0];

        if (!file) {
            if (preview) {
                preview.innerHTML = "";
            }
            return;
        }

        if (!file.type.startsWith("image/")) {
            showMessage("Please select a valid image file.", "error");
            imageInput.value = "";
            return;
        }

        if (file.size > 5 * 1024 * 1024) {
            showMessage("Image size must be less than 5 MB.", "error");
            imageInput.value = "";
            return;
        }

        if (preview) {
            const reader = new FileReader();

            reader.onload = function (event) {
                preview.innerHTML = `
                    <img
                        src="${event.target.result}"
                        alt="Outfit preview"
                        class="outfit-preview"
                    >
                `;
            };

            reader.readAsDataURL(file);
        }
    });
}


// ============================================================
// DISPLAY RECOMMENDATIONS
// ============================================================

function displayRecommendations(result) {
    const container =
        document.getElementById("recommendationsContainer") ||
        document.getElementById("results");

    if (!container) {
        console.log("Recommendation result:", result);
        return;
    }

    container.innerHTML = "";

    const title = document.createElement("h2");
    title.textContent = result.title || "Your Recommendations";

    const summary = document.createElement("p");
    summary.textContent =
        result.summary || "Here are your personalized recommendations.";

    container.appendChild(title);
    container.appendChild(summary);

    if (result.budget !== undefined) {
        const budgetInfo = document.createElement("div");

        budgetInfo.className = "budget-summary";

        budgetInfo.innerHTML = `
            <div>
                <strong>Budget</strong>
                <span>₹${formatNumber(result.budget)}</span>
            </div>

            <div>
                <strong>Estimated Total</strong>
                <span>₹${formatNumber(result.estimated_total || 0)}</span>
            </div>
        `;

        container.appendChild(budgetInfo);
    }

    const recommendations =
        result.recommendations ||
        result.products ||
        [];

    if (!recommendations.length) {
        const emptyMessage = document.createElement("p");

        emptyMessage.textContent =
            "No recommendations were returned. Please try different preferences.";

        container.appendChild(emptyMessage);
        return;
    }

    const grid = document.createElement("div");

    grid.className = "recommendations-grid";

    recommendations.forEach(item => {
        const card = createRecommendationCard(item);
        grid.appendChild(card);
    });

    container.appendChild(grid);

    container.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


// ============================================================
// RECOMMENDATION CARD
// ============================================================

function createRecommendationCard(item) {
    const card = document.createElement("div");

    card.className = "recommendation-card";

    const name = escapeHTML(item.name || "Recommended Item");
    const category = escapeHTML(item.category || "General");
    const platform = escapeHTML(item.platform || "Available Online");
    const description =
        escapeHTML(item.description || "Recommended based on your preferences.");

    const price = Number(item.price || 0);

    card.innerHTML = `
        <div class="recommendation-card-content">

            <span class="recommendation-category">
                ${category}
            </span>

            <h3>${name}</h3>

            <p class="recommendation-description">
                ${description}
            </p>

            <div class="recommendation-footer">

                <strong class="recommendation-price">
                    ₹${formatNumber(price)}
                </strong>

                <span class="recommendation-platform">
                    ${platform}
                </span>

            </div>

            ${
                item.link
                    ? `
                    <a
                        href="${escapeAttribute(item.link)}"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="view-product-btn"
                    >
                        View Option
                    </a>
                    `
                    : ""
            }

        </div>
    `;

    return card;
}


// ============================================================
// LOADING STATE
// ============================================================

function setLoading(button, loading) {
    if (!button) {
        return;
    }

    if (loading) {
        button.dataset.originalText = button.textContent;

        button.disabled = true;
        button.textContent = "Generating...";
        button.classList.add("loading");

    } else {
        button.disabled = false;

        button.textContent =
            button.dataset.originalText || "Generate Recommendations";

        button.classList.remove("loading");
    }
}


// ============================================================
// MESSAGE
// ============================================================

function showMessage(message, type = "info") {
    let messageContainer =
        document.getElementById("messageContainer");

    if (!messageContainer) {
        messageContainer = document.createElement("div");

        messageContainer.id = "messageContainer";

        document.body.prepend(messageContainer);
    }

    messageContainer.innerHTML = "";

    const messageElement = document.createElement("div");

    messageElement.className = `alert alert-${type}`;

    messageElement.textContent = message;

    messageContainer.appendChild(messageElement);

    setTimeout(() => {
        messageElement.remove();
    }, 5000);
}


// ============================================================
// NUMBER FORMATTER
// ============================================================

function formatNumber(number) {
    const value = Number(number);

    if (Number.isNaN(value)) {
        return "0";
    }

    return value.toLocaleString("en-IN", {
        maximumFractionDigits: 2
    });
}


// ============================================================
// HTML SECURITY HELPERS
// ============================================================

function escapeHTML(value) {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


function escapeAttribute(value) {
    return String(value)
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


// ============================================================
// LOGOUT
// ============================================================

async function logout() {
    try {
        const response = await fetch("/api/auth/logout", {
            method: "POST"
        });

        if (response.ok) {
            window.location.href = "/login";
        } else {
            showMessage("Unable to logout.", "error");
        }

    } catch (error) {
        console.error("Logout error:", error);
        showMessage("Something went wrong while logging out.", "error");
    }
}


// ============================================================
// GLOBAL EXPORTS
// ============================================================

window.logout = logout;
window.showMessage = showMessage;