from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import uuid
import datetime
import asgi

app = FastAPI(title="CataL1st OS API")

# --- DATA MODELS ---
class Task(BaseModel):
    id: str
    title: str
    tag: str = "System"
    date: str
    completed: bool = False

class Expense(BaseModel):
    id: str
    title: str
    amount: int

class Note(BaseModel):
    id: str
    content: str

class BackupData(BaseModel):
    tasks: List[Task]
    expenses: List[Expense]
    notes: List[Note]
    study_minutes: int

# --- IN-MEMORY DATABASE ---
db = {
    "tasks": [],
    "expenses": [],
    "notes": [],
    "study_minutes": 0
}

# --- API ROUTES ---
@app.get("/api/data")
async def get_all_data():
    return db

@app.post("/api/tasks")
async def add_task(task_in: dict):
    new_task = Task(
        id=str(uuid.uuid4()),
        title=task_in["title"],
        tag=task_in.get("tag", "System"),
        date=task_in["date"]
    )
    db["tasks"].append(new_task)
    return new_task

@app.put("/api/tasks/{task_id}/toggle")
async def toggle_task(task_id: str):
    for t in db["tasks"]:
        if t.id == task_id:
            t.completed = not t.completed
            return t
    return {"error": "Not found"}

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: str):
    db["tasks"] = [t for t in db["tasks"] if t.id != task_id]
    return {"status": "deleted"}

@app.post("/api/expenses")
async def add_expense(exp_in: dict):
    new_exp = Expense(
        id=str(uuid.uuid4()),
        title=exp_in["title"],
        amount=exp_in["amount"]
    )
    db["expenses"].append(new_exp)
    return new_exp

@app.delete("/api/expenses/{exp_id}")
async def delete_expense(exp_id: str):
    db["expenses"] = [e for e in db["expenses"] if e.id != exp_id]
    return {"status": "deleted"}

@app.post("/api/notes")
async def save_note(note_in: dict):
    if db["notes"]:
        db["notes"][0].content = note_in["content"]
    else:
        db["notes"].append(Note(id=str(uuid.uuid4()), content=note_in["content"]))
    return {"status": "saved"}

@app.post("/api/study")
async def add_study_time(time_in: dict):
    db["study_minutes"] += time_in.get("minutes", 0)
    return {"study_minutes": db["study_minutes"]}

@app.post("/api/backup")
async def restore_backup(backup: BackupData):
    global db
    db["tasks"] = backup.tasks
    db["expenses"] = backup.expenses
    db["notes"] = backup.notes
    db["study_minutes"] = backup.study_minutes
    return {"status": "restored"}

# --- FRONTEND UI ---
@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    html_content = """
    <!DOCTYPE html>
    <html lang="en" class="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CataL1st OS</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&family=Inter:wght@400;500;600;700&display=swap');
            body { font-family: 'Inter', sans-serif; background-color: #09090b; color: #f8fafc; }
            .font-mono { font-family: 'JetBrains Mono', monospace; }
            .panel { background-color: #18181b; border: 1px solid #27272a; }
            ::-webkit-scrollbar { width: 4px; }
            ::-webkit-scrollbar-track { background: #09090b; }
            ::-webkit-scrollbar-thumb { background: #3f3f46; border-radius: 2px; }
            .glow-text { text-shadow: 0 0 10px rgba(34, 211, 238, 0.4); }
        </style>
    </head>
    <body class="h-screen overflow-hidden flex flex-col">
        <div id="app" class="flex flex-col w-full h-full">
            
            <!-- Top Navigation -->
            <header class="panel border-b border-zinc-800 px-6 py-4 flex justify-between items-center shrink-0">
                <div class="flex items-center space-x-4">
                    <div class="w-10 h-10 bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 rounded-lg flex items-center justify-center font-bold text-xl shadow-[0_0_15px_rgba(34,211,238,0.2)]">
                        <i class="fa-solid fa-terminal text-sm"></i>
                    </div>
                    <div>
                        <h1 class="text-xl font-bold font-mono tracking-tight glow-text text-cyan-400">CataL1st_OS</h1>
                        <p class="text-xs text-zinc-400 font-mono">STATUS: ONLINE // NQU CSIE NODE</p>
                    </div>
                </div>
                
                <div class="flex items-center space-x-4">
                    <button @click="downloadBackup" class="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 border border-zinc-700 rounded-md text-xs font-mono text-zinc-300 transition">
                        <i class="fa-solid fa-download mr-2"></i>EXPORT_DATA
                    </button>
                    <label class="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 border border-zinc-700 rounded-md text-xs font-mono text-zinc-300 transition cursor-pointer">
                        <i class="fa-solid fa-upload mr-2"></i>IMPORT_DATA
                        <input type="file" @change="restoreBackup" class="hidden" accept=".json">
                    </label>
                    <div class="h-8 w-px bg-zinc-700 mx-2"></div>
                    <div class="flex items-center space-x-3">
                        <div class="text-right hidden md:block">
                            <p class="font-bold text-sm leading-tight">Sam 范權榮</p>
                            <p class="text-xs text-cyan-400 font-mono">ADMIN</p>
                        </div>
                        <div class="w-10 h-10 rounded-md bg-zinc-800 border border-zinc-700 flex items-center justify-center font-bold">
                            <i class="fa-solid fa-user text-zinc-400"></i>
                        </div>
                    </div>
                </div>
            </header>

            <!-- Main Content Grid -->
            <main class="flex-1 h-full overflow-y-auto p-6 relative flex flex-col gap-6">
                
                <!-- Metrics -->
                <div class="grid grid-cols-4 gap-4 shrink-0">
                    <div class="panel p-5 rounded-lg border-l-2 border-l-cyan-500">
                        <p class="text-xs font-mono text-zinc-400 mb-1 uppercase">Active Directives</p>
                        <div class="flex items-end space-x-3">
                            <p class="text-3xl font-bold font-mono text-zinc-100">{{ openTasksCount }}</p>
                            <p class="text-sm text-zinc-500 font-mono mb-1">PENDING</p>
                        </div>
                    </div>
                    <div class="panel p-5 rounded-lg border-l-2 border-l-rose-500">
                        <p class="text-xs font-mono text-zinc-400 mb-1 uppercase">Critical Priority</p>
                        <div class="flex items-end space-x-3">
                            <p class="text-3xl font-bold font-mono text-zinc-100">{{ dueSoonCount }}</p>
                            <p class="text-sm text-zinc-500 font-mono mb-1">DUE TODAY</p>
                        </div>
                    </div>
                    <div class="panel p-5 rounded-lg border-l-2 border-l-purple-500">
                        <p class="text-xs font-mono text-zinc-400 mb-1 uppercase">Compute Time</p>
                        <div class="flex items-end space-x-3">
                            <p class="text-3xl font-bold font-mono text-zinc-100">{{ db.study_minutes }}</p>
                            <p class="text-sm text-zinc-500 font-mono mb-1">MINUTES</p>
                        </div>
                    </div>
                    <div class="panel p-5 rounded-lg border-l-2 border-l-emerald-500">
                        <p class="text-xs font-mono text-zinc-400 mb-1 uppercase">Resource Drain</p>
                        <div class="flex items-end space-x-3">
                            <p class="text-3xl font-bold font-mono text-zinc-100">{{ totalExpenses }}</p>
                            <p class="text-sm text-zinc-500 font-mono mb-1">NT$</p>
                        </div>
                    </div>
                </div>

                <!-- Three Column Layout -->
                <div class="grid grid-cols-12 gap-6 flex-1 min-h-0">
                    
                    <!-- Directives (Tasks) -->
                    <div class="col-span-5 panel rounded-lg flex flex-col h-full overflow-hidden">
                        <div class="p-4 border-b border-zinc-800 bg-zinc-900/50">
                            <h3 class="text-sm font-bold font-mono text-cyan-400"><i class="fa-solid fa-list-check mr-2"></i>SYS_DIRECTIVES</h3>
                        </div>
                        <div class="p-4">
                            <form @submit.prevent="addTask" class="flex space-x-2">
                                <input v-model="newTask.title" type="text" placeholder="Initialize task..." class="flex-1 bg-zinc-900 border border-zinc-700 px-3 py-2 rounded-md focus:outline-none focus:border-cyan-500 text-sm font-mono transition" required>
                                <input v-model="newTask.date" type="date" class="bg-zinc-900 border border-zinc-700 px-3 py-2 rounded-md text-sm font-mono focus:outline-none focus:border-cyan-500 transition [color-scheme:dark]" required>
                                <button type="submit" class="bg-cyan-600/20 text-cyan-400 border border-cyan-500/50 px-3 py-2 rounded-md text-sm hover:bg-cyan-600/40 transition"><i class="fa-solid fa-plus"></i></button>
                            </form>
                        </div>
                        <div class="flex-1 overflow-y-auto p-4 pt-0 space-y-2">
                            <div v-for="task in sortedTasks" :key="task.id" class="group flex items-start justify-between p-3 rounded-md border transition-all" :class="task.completed ? 'bg-zinc-900 border-zinc-800 opacity-50' : 'bg-zinc-800 border-zinc-700 hover:border-cyan-500/50'">
                                <div class="flex items-start space-x-3">
                                    <button @click="toggleTask(task.id)" class="mt-0.5 w-4 h-4 rounded-sm border flex items-center justify-center transition" :class="task.completed ? 'bg-cyan-500 border-cyan-500 text-zinc-900' : 'border-zinc-500 text-transparent'">
                                        <i class="fa-solid fa-check text-[10px]"></i>
                                    </button>
                                    <div>
                                        <p class="text-sm font-medium" :class="task.completed ? 'line-through text-zinc-500' : 'text-zinc-200'">{{ task.title }}</p>
                                        <p class="text-xs text-zinc-500 font-mono mt-1">EXECUTE_BY: {{ formatDate(task.date) }}</p>
                                    </div>
                                </div>
                                <button @click="deleteTask(task.id)" class="text-zinc-600 hover:text-rose-500 transition opacity-0 group-hover:opacity-100"><i class="fa-solid fa-trash text-xs"></i></button>
                            </div>
                            <div v-if="db.tasks.length === 0" class="text-center py-10 text-zinc-600 font-mono text-sm">NO ACTIVE DIRECTIVES.</div>
                        </div>
                    </div>

                    <!-- Middle Column: Focus & Expenses -->
                    <div class="col-span-4 flex flex-col gap-6 h-full">
                        <!-- Focus Protocol -->
                        <div class="panel rounded-lg shrink-0">
                            <div class="p-4 border-b border-zinc-800 bg-zinc-900/50">
                                <h3 class="text-sm font-bold font-mono text-purple-400"><i class="fa-solid fa-microchip mr-2"></i>FOCUS_PROTOCOL</h3>
                            </div>
                            <div class="p-6 text-center">
                                <div class="text-6xl font-bold font-mono tracking-tighter mb-4" :class="timerRunning ? 'text-purple-400 glow-text' : 'text-zinc-300'">
                                    {{ formattedTime }}
                                </div>
                                <div class="flex justify-center space-x-3">
                                    <button @click="toggleTimer" class="px-4 py-2 border rounded-md text-xs font-mono font-bold transition" :class="timerRunning ? 'border-amber-500/50 text-amber-400 bg-amber-500/10 hover:bg-amber-500/20' : 'border-purple-500/50 text-purple-400 bg-purple-500/10 hover:bg-purple-500/20'">
                                        {{ timerRunning ? 'SUSPEND' : 'INITIALIZE' }}
                                    </button>
                                    <button @click="resetTimer" class="px-4 py-2 border border-zinc-700 bg-zinc-800 text-zinc-400 rounded-md text-xs font-mono font-bold hover:bg-zinc-700 transition">
                                        TERMINATE
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- Finance Log -->
                        <div class="panel rounded-lg flex-1 flex flex-col min-h-0">
                            <div class="p-4 border-b border-zinc-800 bg-zinc-900/50">
                                <h3 class="text-sm font-bold font-mono text-emerald-400"><i class="fa-solid fa-money-bill-wave mr-2"></i>FINANCE_LOG</h3>
                            </div>
                            <div class="p-4 pb-2">
                                <form @submit.prevent="addExpense" class="flex space-x-2">
                                    <input v-model="newExpense.title" type="text" placeholder="Asset..." class="w-1/2 bg-zinc-900 border border-zinc-700 px-3 py-1.5 rounded-md text-sm font-mono focus:outline-none focus:border-emerald-500" required>
                                    <input v-model.number="newExpense.amount" type="number" placeholder="Cost" class="w-1/3 bg-zinc-900 border border-zinc-700 px-3 py-1.5 rounded-md text-sm font-mono focus:outline-none focus:border-emerald-500" required>
                                    <button type="submit" class="w-1/6 bg-emerald-600/20 text-emerald-400 border border-emerald-500/50 rounded-md hover:bg-emerald-600/40 transition"><i class="fa-solid fa-plus text-xs"></i></button>
                                </form>
                            </div>
                            <div class="flex-1 overflow-y-auto p-4 pt-0 space-y-1">
                                <div v-for="exp in db.expenses" :key="exp.id" class="flex justify-between items-center p-2 hover:bg-zinc-800 rounded-md group">
                                    <p class="text-sm text-zinc-300 font-mono">{{ exp.title }}</p>
                                    <div class="flex items-center space-x-3">
                                        <p class="font-bold text-sm text-emerald-400 font-mono">${{ exp.amount }}</p>
                                        <button @click="deleteExpense(exp.id)" class="text-zinc-600 hover:text-rose-500 opacity-0 group-hover:opacity-100 transition"><i class="fa-solid fa-xmark text-xs"></i></button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Scratchpad -->
                    <div class="col-span-3 panel rounded-lg flex flex-col h-full">
                        <div class="p-4 border-b border-zinc-800 bg-zinc-900/50">
                            <h3 class="text-sm font-bold font-mono text-zinc-400"><i class="fa-solid fa-pen-nib mr-2"></i>SCRATCHPAD</h3>
                        </div>
                        <textarea v-model="quickNote" @blur="saveNote" placeholder="> Enter log output here..." class="flex-1 w-full bg-transparent p-4 text-sm font-mono text-zinc-300 focus:outline-none resize-none leading-relaxed"></textarea>
                    </div>

                </div>
            </main>
        </div>

        <script>
            const { createApp } = Vue
            createApp({
                data() {
                    return {
                        db: { tasks: [], expenses: [], notes: [], study_minutes: 0 },
                        newTask: { title: '', date: new Date().toISOString().split('T')[0] },
                        newExpense: { title: '', amount: null },
                        quickNote: '',
                        
                        timeLeft: 25 * 60,
                        timerRunning: false,
                        timerInterval: null
                    }
                },
                computed: {
                    sortedTasks() {
                        return this.db.tasks.slice().sort((a, b) => new Date(a.date) - new Date(b.date));
                    },
                    openTasksCount() {
                        return this.db.tasks.filter(t => !t.completed).length;
                    },
                    dueSoonCount() {
                        const today = new Date().toISOString().split('T')[0];
                        return this.db.tasks.filter(t => !t.completed && t.date === today).length;
                    },
                    totalExpenses() {
                        return this.db.expenses.reduce((sum, exp) => sum + exp.amount, 0);
                    },
                    formattedTime() {
                        const m = Math.floor(this.timeLeft / 60).toString().padStart(2, '0');
                        const s = (this.timeLeft % 60).toString().padStart(2, '0');
                        return `${m}:${s}`;
                    }
                },
                mounted() {
                    this.fetchData();
                },
                methods: {
                    async fetchData() {
                        const res = await fetch('/api/data');
                        this.db = await res.json();
                        if (this.db.notes.length > 0) this.quickNote = this.db.notes[0].content;
                    },
                    formatDate(dateStr) {
                        return new Date(dateStr).toISOString().split('T')[0];
                    },
                    async addTask() {
                        const res = await fetch('/api/tasks', {
                            method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(this.newTask)
                        });
                        const data = await res.json();
                        this.db.tasks.push(data);
                        this.newTask.title = '';
                    },
                    async toggleTask(id) {
                        await fetch(`/api/tasks/${id}/toggle`, { method: 'PUT' });
                        const t = this.db.tasks.find(x => x.id === id);
                        if (t) t.completed = !t.completed;
                    },
                    async deleteTask(id) {
                        await fetch(`/api/tasks/${id}`, { method: 'DELETE' });
                        this.db.tasks = this.db.tasks.filter(t => t.id !== id);
                    },
                    async addExpense() {
                        const res = await fetch('/api/expenses', {
                            method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(this.newExpense)
                        });
                        const data = await res.json();
                        this.db.expenses.unshift(data);
                        this.newExpense = { title: '', amount: null };
                    },
                    async deleteExpense(id) {
                        await fetch(`/api/expenses/${id}`, { method: 'DELETE' });
                        this.db.expenses = this.db.expenses.filter(e => e.id !== id);
                    },
                    async saveNote() {
                        await fetch('/api/notes', {
                            method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({content: this.quickNote})
                        });
                    },
                    toggleTimer() {
                        if (this.timerRunning) {
                            clearInterval(this.timerInterval);
                            this.timerRunning = false;
                        } else {
                            this.timerRunning = true;
                            this.timerInterval = setInterval(() => {
                                if (this.timeLeft > 0) {
                                    this.timeLeft--;
                                } else {
                                    this.completeSession();
                                }
                            }, 1000);
                        }
                    },
                    resetTimer() {
                        clearInterval(this.timerInterval);
                        this.timerRunning = false;
                        this.timeLeft = 25 * 60;
                    },
                    async completeSession() {
                        this.resetTimer();
                        const res = await fetch('/api/study', {
                            method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({minutes: 25})
                        });
                        const data = await res.json();
                        this.db.study_minutes = data.study_minutes;
                        alert("PROTOCOL COMPLETE. LOGGED 25 MINS.");
                    },
                    downloadBackup() {
                        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(this.db));
                        const downloadAnchorNode = document.createElement('a');
                        downloadAnchorNode.setAttribute("href", dataStr);
                        downloadAnchorNode.setAttribute("download", "catal1st_sys_backup.json");
                        document.body.appendChild(downloadAnchorNode);
                        downloadAnchorNode.click();
                        downloadAnchorNode.remove();
                    },
                    restoreBackup(event) {
                        const file = event.target.files[0];
                        if (!file) return;
                        const reader = new FileReader();
                        reader.onload = async (e) => {
                            try {
                                const backup = JSON.parse(e.target.result);
                                await fetch('/api/backup', {
                                    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(backup)
                                });
                                this.fetchData();
                                alert("SYSTEM DATA RESTORED.");
                            } catch (err) {
                                alert("ERR: INVALID BACKUP FILE.");
                            }
                        };
                        reader.readAsText(file);
                        event.target.value = '';
                    }
                }
            }).mount('#app')
        </script>
    </body>
    </html>
    """
    return html_content

async def on_fetch(request, env):
    return await asgi.fetch(app, request, env)
