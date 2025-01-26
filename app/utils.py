import subprocess
import logging

def ensure_worker_running(user_id):
    worker_name = f"worker_user_{user_id}"
    try:
        # Check if worker container exists
        existing_container = subprocess.run(
            ["docker", "ps", "-a", "-f", f"name={worker_name}", "--format", "{{.Status}}"],
            capture_output=True, text=True
        )
        
        if existing_container.stdout.strip():
            # Container exists, check if running
            if "Up" not in existing_container.stdout:
                # Start the stopped container
                subprocess.run(["docker", "start", worker_name], check=True)
            return True
        
        # Create new worker container
        subprocess.run([
            "docker", "run", "-d", 
            "--name", worker_name, 
            "--network", "ezroi_default", 
            "-e", f"USER_ID={user_id}",
            "ezroi_worker", 
            "celery", "-A", "app.celery_app", "worker", 
            "-Q", f"worker_user_{user_id}"
        ], check=True)
        
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error managing worker for user {user_id}: {e}")
        return False