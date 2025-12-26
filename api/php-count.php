<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle OPTIONS request for CORS
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

// Путь к файлу счетчика (относительно корня проекта)
$counterFile = dirname(__DIR__) . '/php/counter.txt';
$counterDir = dirname($counterFile);

// Создаем папку если её нет
if (!file_exists($counterDir)) {
    mkdir($counterDir, 0755, true);
}

// Убеждаемся, что файл существует и создаем его если нет
if (!file_exists($counterFile)) {
    file_put_contents($counterFile, '0');
    chmod($counterFile, 0644);
}

// Получаем текущее значение счетчика
function getCount() {
    global $counterFile;
    if (file_exists($counterFile)) {
        $count = file_get_contents($counterFile);
        return intval($count);
    }
    return 0;
}

// Увеличиваем счетчик
function incrementCount() {
    global $counterFile;
    $currentCount = getCount();
    $newCount = $currentCount + 1;
    file_put_contents($counterFile, $newCount);
    return $newCount;
}

// Обработка GET запроса - получить счетчик
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $count = getCount();
    echo json_encode(['count' => $count]);
    exit;
}

// Обработка POST запроса - увеличить счетчик
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    try {
        $newCount = incrementCount();
        echo json_encode(['success' => true, 'count' => $newCount]);
    } catch (Exception $e) {
        http_response_code(500);
        echo json_encode(['error' => $e->getMessage(), 'success' => false]);
    }
    exit;
}

// Если метод не поддерживается
http_response_code(405);
echo json_encode(['error' => 'Method not allowed']);
?>

