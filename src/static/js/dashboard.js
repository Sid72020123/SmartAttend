"use strict";

// Message auto-closing code by an AI agent:
document.querySelectorAll(".message").forEach((message) => {
    const closeMessage = () => {
        message.classList.add("hidden");
    };

    message.querySelector(".message-close")?.addEventListener("click", closeMessage);
    window.setTimeout(closeMessage, 20_000);
});

// Time formatter and humanize script created by an AI agent:
const relativeTimeFormatter = new Intl.RelativeTimeFormat(undefined, {
    numeric: "auto",
});

function humanizeTimestamp(timestamp) {
    const differenceInSeconds = (Date.parse(timestamp) - Date.now()) / 1000;
    const units = [
        ["year", 60 * 60 * 24 * 365],
        ["month", 60 * 60 * 24 * 30],
        ["day", 60 * 60 * 24],
        ["hour", 60 * 60],
        ["minute", 60],
        ["second", 1],
    ];

    for (const [unit, secondsPerUnit] of units) {
        if (Math.abs(differenceInSeconds) >= secondsPerUnit || unit === "second") {
            return relativeTimeFormatter.format(Math.round(differenceInSeconds / secondsPerUnit), unit);
        }
    }
}

document.querySelectorAll(".event-created-at").forEach((element) => {
    const timestamp = element.getAttribute("datetime");
    if (!timestamp) {
        return;
    }

    const parsedTimestamp = Date.parse(timestamp);
    if (Number.isNaN(parsedTimestamp)) {
        return;
    }

    element.textContent = humanizeTimestamp(timestamp);
    element.title = new Date(parsedTimestamp).toLocaleString();
});

// For event management:
const input = document.getElementById("event-title");
const editBtn = document.getElementById("edit-toggle");
const saveBtn = document.getElementById("save-btn");

const eventStatus = document.getElementById("event-status");

if (input && editBtn && saveBtn) {
    editBtn.addEventListener("click", () => {
        input.removeAttribute("readonly");
        input.focus();
        editBtn.style.display = "none";
        saveBtn.style.display = "inline-block";
    });
}

if (eventStatus) {
    eventStatus.addEventListener("change", () => {
        saveBtn.style.display = "inline-block";
    });
}
