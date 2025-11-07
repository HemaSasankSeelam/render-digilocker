from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core.handlers.wsgi import WSGIRequest
# Create your views here.
import selenium_script as selenium_script
from .models import running_status,completed
import threading


def home(request):

    if not running_status.objects.last().is_running:
        threading.Thread(target=selenium_script.run_script, daemon=True).start()
    
    
    return HttpResponse("""
    <html>
        <body>
            <h2>Live Status</h2>
            <pre id="data"></pre>
            <script>
            async function update() {
                const res = await fetch('/status');
                const data = await res.json();
                document.getElementById('data').innerText = JSON.stringify(data, null, 2);
            }
            setInterval(update, 800);  // every 800 milli second
            update();
            </script>
        </body>
        </html>
        """)

def status(request:WSGIRequest):

    last = completed.objects.last()
    last_completed = last.text if last != None else None
    return JsonResponse({"is_running": running_status.objects.last().is_running, 
            "last completed": last_completed})