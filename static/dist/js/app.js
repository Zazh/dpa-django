// 1) Регистрируем плагин
gsap.registerPlugin(ScrollTrigger);

const DEBUG = false;
if (DEBUG) {
    ScrollTrigger.defaults({ markers: true }); // покажет start/end на экране
}

// 3) Небольшая «санити»-проверка в консоли
console.log("GSAP", gsap.version, "ScrollTrigger", ScrollTrigger.version);

const video = document.getElementById("videoEl");

// Убедимся, что начальное состояние — со скруглением
video.classList.add("rounded-xl");
video.classList.remove("rounded-none");

// Анимация увеличения ширины + запуск видео на финише
gsap.to(".hero-video__el", {
    width: "100%",
    ease: "none",
    scrollTrigger: {
        trigger: ".hero-video__el",
        start: "top 80%",
        end: "top 20%",
        scrub: true,
        markers: DEBUG
    },
    onStart: () => {
        // при входе в диапазон анимации держим скруглённые углы
        video.classList.add("rounded-xl");
        video.classList.remove("rounded-none");
    },
    onComplete: () => {
        // достигли 100% — убираем скругление и запускаем видео
        video.classList.remove("rounded-xl");
        video.classList.add("rounded-none");
        const p = video.play();
        if (p && typeof p.catch === "function") {
            p.catch(() => {/* молча игнорим, если браузер заблокировал автоплей */});
        }
    },
    onReverseComplete: () => {
        // вернулись к 80% — возвращаем скруглённые углы
        video.classList.add("rounded-xl");
        video.classList.remove("rounded-none");
        // при желании можно сбрасывать проигрывание:
        video.pause();
        // video.currentTime = 0;
    }
});

// Остановка видео, когда секция ушла вверх из вьюпорта
ScrollTrigger.create({
    trigger: ".hero-video__el",
    start: "bottom top",
    onEnterBack: () => {
        const p = video.play();
        if (p && typeof p.catch === "function") p.catch(() => {});
    },
    onLeave: () => video.pause()
});

// заливаем текст слева-направо по скроллу
const lines = gsap.utils.toArray("#slogan .progress-text__fill .line");
lines.forEach(el => el.style.setProperty("--p", "0%"));

// строим таймлайн: каждая строка заполняется по очереди
const tl = gsap.timeline({
    defaults: { ease: "none", duration: 1 },
    scrollTrigger: {
        trigger: "#slogan",
        start: "top 60%",
        end: "bottom 20%", // весь таймлайн растянут от старта до конца
        scrub: true,
        // markers: true
    }
});

// последовательно анимируем переменную каждой строки
lines.forEach(line => {
    tl.to(line, { "--p": "100%" }, ">"); // ">" = начинать после предыдущей
});

gsap.set("#hero-text", { transformOrigin: "50% 0%" }); // сверху по центру

gsap.to("#hero-text", {
    scale: 0.85,          // во сколько раз уменьшить к концу диапазона
    yPercent: -10,        // лёгкий уезд вверх (эффект «отдаления»)
    opacity: 0.95,        // можно убрать, если не нужно
    ease: "none",
    scrollTrigger: {
        trigger: ".hero-video__el",
        start: "top 80%",
        end:   "top 20%",
        scrub: true,
        markers: DEBUG
    }
});


// форматирование числа с учётом локали и десятичных знаков
function formatNumber(val, decimals = 0) {
    return Number(val).toLocaleString('ru-RU', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    });
}

function animateCounter(el) {
    const start    = Number(el.dataset.start ?? 0);
    const end      = Number(el.dataset.end ?? 0);
    const duration = Number(el.dataset.duration ?? 1.2);
    const decimals = parseInt(el.dataset.decimals ?? 0, 10);
    const prefix   = el.dataset.prefix ?? '';
    const suffix   = el.dataset.suffix ?? '';

    if (isNaN(end)) return; // защита от ошибок

    // уважим prefers-reduced-motion: сразу выставим конечное значение
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        el.textContent = `${prefix}${formatNumber(end, decimals)}${suffix}`;
        return;
    }

    const obj = { val: start };
    gsap.to(obj, {
        val: end,
        duration,
        ease: 'power1.out',
        onUpdate: () => {
            const displayVal = decimals ? obj.val.toFixed(decimals) : Math.round(obj.val);
            el.textContent = `${prefix}${formatNumber(displayVal, decimals)}${suffix}`;
        }
    });
}

// создаём триггеры для всех .counter, запускаем один раз при входе
gsap.utils.toArray('.counter').forEach(el => {
    // сброс начального текста (на всякий случай)
    const start = Number(el.dataset.start ?? 0);
    const decimals = parseInt(el.dataset.decimals ?? 0, 10);
    const prefix = el.dataset.prefix ?? '';
    const suffix = el.dataset.suffix ?? '';
    el.textContent = `${prefix}${formatNumber(start, decimals)}${suffix}`;

    ScrollTrigger.create({
        trigger: el,
        start: 'top 85%',
        once: true,            // запустить один раз
        // markers: true,      // включи для дебага
        onEnter: () => animateCounter(el)
    });
});

