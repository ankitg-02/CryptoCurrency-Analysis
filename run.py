import time
import webbrowser
from threading import Timer
from app import create_app

def start_browser(port):
    """Open browser after server starts"""
    webbrowser.open(f'http://127.0.0.1:{port}/')

if __name__ == '__main__':
    # Print startup message
    print("Starting Cryptocurrency Analysis App...")
    start_time = time.time()
    
    port = 5000
    app = create_app()
    
    # Open browser after a short delay
    Timer(1.5, start_browser, args=[port]).start()
    
    print(f"Server starting at http://127.0.0.1:{port}/")
    print(f"Startup time: {time.time() - start_time:.2f} seconds")
    
    # Run with optimized settings
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True,
        use_reloader=False,  # Disable reloader for faster startup
        threaded=True  # Enable threading for better performance
    )
