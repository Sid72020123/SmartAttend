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

const copyCheckinLinkButton = document.getElementById("copy-checkin-link");
const shareCheckinImageButton = document.getElementById("share-checkin-image");
const checkinActionStatus = document.getElementById("checkin-action-status");

function setCheckinActionStatus(message) {
    if (checkinActionStatus) {
        checkinActionStatus.textContent = message;
    }
}

if (copyCheckinLinkButton) {
    copyCheckinLinkButton.addEventListener("click", async () => {
        const text = copyCheckinLinkButton.dataset.copyText;
        if (!text) {
            return;
        }

        try {
            await navigator.clipboard.writeText(text);
        } catch {
            const urlInput = document.getElementById("checkin-url");
            urlInput.focus();
            urlInput.select();
            document.execCommand("copy");
            urlInput.setSelectionRange(0, 0);
        }

        setCheckinActionStatus("Check-in link copied.");
    });
}

if (shareCheckinImageButton) {
    shareCheckinImageButton.addEventListener("click", async () => {
        const imageUrl = shareCheckinImageButton.dataset.imageUrl;
        const eventTitle = shareCheckinImageButton.dataset.eventTitle || "Event";
        const checkinUrl = shareCheckinImageButton.dataset.checkinUrl;

        if (!imageUrl) {
            return;
        }

        try {
            const response = await fetch(imageUrl);
            if (!response.ok) {
                throw new Error("Unable to load the QR image.");
            }

            const imageBlob = await response.blob();
            const imageFile = new File([imageBlob], "checkin-qr.png", {
                type: imageBlob.type || "image/png",
            });

            if (navigator.canShare?.({ files: [imageFile] }) && navigator.share) {
                await navigator.share({
                    title: `${eventTitle} check-in`,
                    text: "Scan this QR code to check in.",
                    files: [imageFile],
                });
                setCheckinActionStatus("QR image shared.");
            } else if (navigator.share) {
                await navigator.share({
                    title: `${eventTitle} check-in`,
                    text: "Use this link to check in.",
                    url: checkinUrl,
                });
                setCheckinActionStatus("Check-in link shared.");
            } else {
                const downloadLink = document.createElement("a");
                downloadLink.href = URL.createObjectURL(imageBlob);
                downloadLink.download = "checkin-qr.png";
                downloadLink.click();
                URL.revokeObjectURL(downloadLink.href);
                setCheckinActionStatus("QR image downloaded because sharing is unavailable.");
            }
        } catch (error) {
            if (error.name !== "AbortError") {
                setCheckinActionStatus("Unable to share the QR image. Use Download QR image instead.");
            }
        }
    });
}
