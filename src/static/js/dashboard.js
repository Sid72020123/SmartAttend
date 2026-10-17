"use strict";

// Time formatter and humanize script created by an AI model:
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
