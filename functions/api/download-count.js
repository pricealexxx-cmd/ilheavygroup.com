// Cloudflare Pages Function для обработки счетчика скачиваний
// Использует KV Storage для хранения счетчика

export async function onRequestGet(context) {
  const { env } = context;
  
  try {
    // Получаем счетчик из KV
    const count = await env.DOWNLOAD_COUNTER.get('count');
    const currentCount = count ? parseInt(count, 10) : 0;
    
    return new Response(JSON.stringify({ count: currentCount }), {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });
  }
}

export async function onRequestPost(context) {
  const { env } = context;
  
  try {
    // Получаем текущее значение
    const count = await env.DOWNLOAD_COUNTER.get('count');
    const currentCount = count ? parseInt(count, 10) : 0;
    
    // Увеличиваем счетчик
    const newCount = currentCount + 1;
    
    // Сохраняем обратно в KV
    await env.DOWNLOAD_COUNTER.put('count', newCount.toString());
    
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

