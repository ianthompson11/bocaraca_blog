document.addEventListener("DOMContentLoaded", () => {
    document.addEventListener("mousemove", (e) => {
        const dot = document.createElement("div");
        dot.className = "cursor-dot";
        dot.style.left = `${e.clientX}px`;
        dot.style.top = `${e.clientY}px`;
        document.body.appendChild(dot);

        setTimeout(() => {
            dot.remove();
        }, 500); // Desaparece después de medio segundo
    });
});