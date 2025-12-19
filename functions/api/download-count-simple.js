// Упрощенная версия без KV - использует встроенное хранилище
// ВНИМАНИЕ: Это временное решение, данные могут теряться при перезапуске

let downloadCount = 0; // Начинаем с 0

export async function onRequestGet(context) {
  try {
    // Попытка получить из KV (если будет настроен)
    let count = 0;
    
    if (context.env?.DOWNLOAD_COUNTER) {
      try {
        const kvCount = await context.env.DOWNLOAD_COUNTER.get('count');
        count = kvCount ? parseInt(kvCount, 10) : 0;
      } catch (e) {
        // Если KV не настроен, используем значение по умолчанию
        count = 0;
      }
    }
    
    // Если KV не работает, используем файл с GitHub или внешний API
    // Пока возвращаем базовое значение
    return new Response(JSON.stringify({ 
      count: count,
      note: count === 0 ? 'KV not configured yet' : null
    }), {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: error.message,
      count: 0 
    }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });
  }
}

export async function onRequestPost(context) {
  try {
    let newCount = 0;
    
    if (context.env?.DOWNLOAD_COUNTER) {
      // Используем KV если доступен
      try {
        const count = await context.env.DOWNLOAD_COUNTER.get('count');
        const currentCount = count ? parseInt(count, 10) : 0;
        newCount = currentCount + 1;
        await context.env.DOWNLOAD_COUNTER.put('count', newCount.toString());
      } catch (e) {
        // Если KV не настроен, просто возвращаем ошибку
        return new Response(JSON.stringify({ 
          error: 'KV namespace not configured. Please set up DOWNLOAD_COUNTER in Cloudflare Pages Settings → Functions → KV Namespace Bindings',
          success: false 
        }), {
          status: 500,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          },
        });
      }
    } else {
      return new Response(JSON.stringify({ 
        error: 'KV namespace not configured. Please set up DOWNLOAD_COUNTER in Cloudflare Pages Settings → Functions → KV Namespace Bindings',
        success: false 
      }), {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      });
    }
    
    return new Response(JSON.stringify({ 
      success: true, 
      count: newCount 
    }), {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
    });
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: error.message,
      success: false 
    }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });
  }
}

export async function onRequestOptions(context) {
  return new Response(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  });
}

