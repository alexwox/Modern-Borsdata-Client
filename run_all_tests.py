   # run_all_tests.py
   import os
   import subprocess
   from dotenv import load_dotenv

   # Load environment variables from .env file
   load_dotenv()

   # Run all tests
   subprocess.run(["python", "-m", "pytest"])