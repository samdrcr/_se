import { useState } from "react";
import { 
  Zap, 
  PlusCircle, 
  ShieldCheck,
  X,
  Trash2,
  Plus
} from "lucide-react";

interface Room {
  id: string;
  name: string;
  occupants: number;
  prevKwh: number;
  currKwh: number;
}

export default function App() {
  const [activeTab, setActiveTab] = useState<"bills" | "expenses" | "maintenance">("bills");

  // 可自由增減的房間清單
  const [rooms, setRooms] = useState<Room[]>([
    { id: "1", name: "1F 套房", occupants: 2, prevKwh: 1200, currKwh: 1350 },
    { id: "2", name: "2F 雅房 A", occupants: 1, prevKwh: 800, currKwh: 880 },
    { id: "3", name: "2F 雅房 B", occupants: 1, prevKwh: 950, currKwh: 1040 },
  ]);

  // 電費狀態
  const [totalBill, setTotalBill] = useState(4850);
  const [totalKwh, setTotalKwh] = useState(1100);

  // 日常雜支代墊清單
  const [expenses, setExpenses] = useState([
    { id: 1, title: "Costco 衛生紙三層 x2", amount: 799, payer: "阿榮", date: "2026-09-20" },
    { id: 2, title: "客廳濾水器濾芯替換", amount: 1200, payer: "柏翰", date: "2026-09-21" },
    { id: 3, title: "專用大垃圾袋與洗碗精", amount: 320, payer: "承恩", date: "2026-09-22" },
  ]);

  // 修繕看板清單
  const [issues, setIssues] = useState([
    { id: 1, title: "1F 浴室蓮蓬頭軟管過短且漏水", status: "已報修房東", reporter: "阿榮" },
    { id: 2, title: "2F 窗外掛衣空間感應燈故障", status: "待處理", reporter: "柏翰" },
  ]);

  // Modal 狀態
  const [showExpenseModal, setShowExpenseModal] = useState(false);
  const [showIssueModal, setShowIssueModal] = useState(false);

  // 表單暫存狀態
  const [newExpenseTitle, setNewExpenseTitle] = useState("");
  const [newExpenseAmount, setNewExpenseAmount] = useState("");
  const [newExpensePayer, setNewExpensePayer] = useState("阿榮");

  const [newIssueTitle, setNewIssueTitle] = useState("");
  const [newIssueReporter, setNewIssueReporter] = useState("阿榮");

  // 房間管理操作
  const handleAddRoom = () => {
    const newRoomNumber = rooms.length + 1;
    const newRoom: Room = {
      id: Date.now().toString(),
      name: `房間 ${newRoomNumber}`,
      occupants: 1,
      prevKwh: 0,
      currKwh: 0,
    };
    setRooms([...rooms, newRoom]);
  };

  const handleDeleteRoom = (id: string) => {
    if (rooms.length <= 1) return; // 至少保留一間
    setRooms(rooms.filter((r) => r.id !== id));
  };

  const handleUpdateRoom = (id: string, field: keyof Room, value: string | number) => {
    setRooms(
      rooms.map((r) => {
        if (r.id === id) {
          return { ...r, [field]: value };
        }
        return r;
      })
    );
  };

  // 獨立電表分拆運算
  const avgRate = totalKwh > 0 ? totalBill / totalKwh : 0;
  const totalPrivateKwh = rooms.reduce((acc, r) => acc + Math.max(0, r.currKwh - r.prevKwh), 0);
  const commonKwh = Math.max(0, totalKwh - totalPrivateKwh);
  const totalOccupants = rooms.reduce((acc, r) => acc + (Number(r.occupants) || 1), 0);
  const commonCostPerPerson = totalOccupants > 0 ? (commonKwh * avgRate) / totalOccupants : 0;

  // 提交新雜支
  const handleAddExpense = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newExpenseTitle || !newExpenseAmount) return;
    const newItem = {
      id: Date.now(),
      title: newExpenseTitle,
      amount: Number(newExpenseAmount),
      payer: newExpensePayer,
      date: new Date().toISOString().split("T")[0],
    };
    setExpenses([newItem, ...expenses]);
    setNewExpenseTitle("");
    setNewExpenseAmount("");
    setShowExpenseModal(false);
  };

  // 提交新修繕
  const handleAddIssue = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newIssueTitle) return;
    const newItem = {
      id: Date.now(),
      title: newIssueTitle,
      status: "待處理",
      reporter: newIssueReporter,
    };
    setIssues([newItem, ...issues]);
    setNewIssueTitle("");
    setShowIssueModal(false);
  };

  return (
    <div className="min-h-screen pb-12 bg-slate-50 text-slate-900">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10 shadow-sm">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-indigo-600 text-white p-2 rounded-xl shadow-md">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold leading-tight">FairShare 室友分帳神器</h1>
              <p className="text-xs text-slate-500">大學外宿生活必備 · 電費獨立拆算 & 雜支平攤</p>
            </div>
          </div>
          <div className="flex bg-slate-100 p-1 rounded-xl gap-1 text-sm font-medium">
            <button
              onClick={() => setActiveTab("bills")}
              className={`px-3 py-1.5 rounded-lg transition-all ${
                activeTab === "bills" ? "bg-white text-indigo-600 shadow-sm" : "text-slate-600 hover:text-slate-900"
              }`}
            >
              水電結算
            </button>
            <button
              onClick={() => setActiveTab("expenses")}
              className={`px-3 py-1.5 rounded-lg transition-all ${
                activeTab === "expenses" ? "bg-white text-indigo-600 shadow-sm" : "text-slate-600 hover:text-slate-900"
              }`}
            >
              日常代墊
            </button>
            <button
              onClick={() => setActiveTab("maintenance")}
              className={`px-3 py-1.5 rounded-lg transition-all ${
                activeTab === "maintenance" ? "bg-white text-indigo-600 shadow-sm" : "text-slate-600 hover:text-slate-900"
              }`}
            >
              合租報修
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-5xl mx-auto px-4 mt-6">
        {activeTab === "bills" && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* 總帳單輸入卡片 */}
            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-4">
              <h2 className="text-base font-bold flex items-center gap-2 text-slate-900">
                <Zap className="w-5 h-5 text-amber-500" /> 台電本期總帳單
              </h2>
              <div>
                <label className="text-xs font-semibold text-slate-600">總金額 (NT$)</label>
                <input
                  type="number"
                  value={totalBill}
                  onChange={(e) => setTotalBill(Number(e.target.value))}
                  className="w-full mt-1 border border-slate-300 rounded-lg px-3 py-2 text-slate-900 font-semibold focus:outline-indigo-500"
                />
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-600">台電總用電度數 (kWh)</label>
                <input
                  type="number"
                  value={totalKwh}
                  onChange={(e) => setTotalKwh(Number(e.target.value))}
                  className="w-full mt-1 border border-slate-300 rounded-lg px-3 py-2 text-slate-900 font-semibold focus:outline-indigo-500"
                />
              </div>
              <div className="bg-amber-50 border border-amber-200 p-3 rounded-xl text-xs text-amber-800 space-y-1">
                <p>⚡ 平均每度單價：<strong>NT$ {avgRate.toFixed(2)}</strong></p>
                <p>🏢 公電總計：<strong>{commonKwh.toFixed(0)} 度</strong></p>
                <p>👥 全室總人數：<strong>{totalOccupants} 人</strong> (每人攤 NT$ {Math.round(commonCostPerPerson)})</p>
              </div>
            </div>

            {/* 房間列表與動態增減 */}
            <div className="md:col-span-2 space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-base font-bold text-slate-900">
                  房間分電表與人數設定 ({rooms.length} 間房)
                </h2>
                <button
                  onClick={handleAddRoom}
                  className="flex items-center gap-1.5 bg-indigo-50 text-indigo-600 hover:bg-indigo-100 text-xs font-semibold px-3 py-1.5 rounded-xl transition"
                >
                  <Plus className="w-4 h-4" /> 新增房間
                </button>
              </div>

              <div className="space-y-3">
                {rooms.map((room) => {
                  const used = Math.max(0, room.currKwh - room.prevKwh);
                  const privateCost = used * avgRate;
                  const roomCommonCost = commonCostPerPerson * room.occupants;
                  const total = Math.round(privateCost + roomCommonCost);
                  const perHead = room.occupants > 0 ? Math.round(total / room.occupants) : 0;

                  return (
                    <div key={room.id} className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm space-y-3">
                      <div className="flex items-center justify-between">
                        <input
                          type="text"
                          value={room.name}
                          onChange={(e) => handleUpdateRoom(room.id, "name", e.target.value)}
                          className="font-bold text-slate-900 border-b border-transparent hover:border-slate-300 focus:border-indigo-500 focus:outline-none px-1"
                        />
                        <div className="flex items-center gap-3">
                          <div className="text-right">
                            <span className="text-base font-bold text-indigo-600">NT$ {total}</span>
                            {room.occupants > 1 && (
                              <span className="text-xs text-slate-400 ml-2">(每人 NT$ {perHead})</span>
                            )}
                          </div>
                          {rooms.length > 1 && (
                            <button
                              onClick={() => handleDeleteRoom(room.id)}
                              className="text-slate-300 hover:text-red-500 transition"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          )}
                        </div>
                      </div>

                      {/* 參數編輯欄 */}
                      <div className="grid grid-cols-3 gap-3 text-xs">
                        <div>
                          <label className="text-slate-500">入住人數</label>
                          <input
                            type="number"
                            min="1"
                            value={room.occupants}
                            onChange={(e) => handleUpdateRoom(room.id, "occupants", Math.max(1, Number(e.target.value)))}
                            className="w-full mt-1 border border-slate-200 rounded-lg p-1.5 font-medium focus:outline-indigo-500"
                          />
                        </div>
                        <div>
                          <label className="text-slate-500">上期指針 (kWh)</label>
                          <input
                            type="number"
                            value={room.prevKwh}
                            onChange={(e) => handleUpdateRoom(room.id, "prevKwh", Number(e.target.value))}
                            className="w-full mt-1 border border-slate-200 rounded-lg p-1.5 font-medium focus:outline-indigo-500"
                          />
                        </div>
                        <div>
                          <label className="text-slate-500">本期指針 (kWh)</label>
                          <input
                            type="number"
                            value={room.currKwh}
                            onChange={(e) => handleUpdateRoom(room.id, "currKwh", Number(e.target.value))}
                            className="w-full mt-1 border border-slate-200 rounded-lg p-1.5 font-medium focus:outline-indigo-500"
                          />
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {activeTab === "expenses" && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-base font-bold text-slate-900">共同日常雜支清單</h2>
              <button 
                onClick={() => setShowExpenseModal(true)}
                className="flex items-center gap-1.5 bg-indigo-600 text-white text-xs font-semibold px-3 py-2 rounded-xl hover:bg-indigo-700 transition"
              >
                <PlusCircle className="w-4 h-4" /> 記錄新代墊款
              </button>
            </div>

            <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
              <table className="w-full text-left text-sm">
                <thead className="bg-slate-50 border-b border-slate-200 text-xs text-slate-500">
                  <tr>
                    <th className="p-3">項目說明</th>
                    <th className="p-3">代墊人</th>
                    <th className="p-3">日期</th>
                    <th className="p-3 text-right">金額</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {expenses.map((item) => (
                    <tr key={item.id} className="hover:bg-slate-50">
                      <td className="p-3 font-medium text-slate-800">{item.title}</td>
                      <td className="p-3 text-slate-600">
                        <span className="bg-indigo-50 text-indigo-700 text-xs px-2 py-0.5 rounded-md font-semibold">
                          {item.payer}
                        </span>
                      </td>
                      <td className="p-3 text-xs text-slate-400">{item.date}</td>
                      <td className="p-3 text-right font-bold text-slate-900">NT$ {item.amount}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === "maintenance" && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-base font-bold text-slate-900">合租報修與公共維護看板</h2>
              <button 
                onClick={() => setShowIssueModal(true)}
                className="flex items-center gap-1.5 bg-indigo-600 text-white text-xs font-semibold px-3 py-2 rounded-xl hover:bg-indigo-700 transition"
              >
                <PlusCircle className="w-4 h-4" /> 回報新問題
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {issues.map((issue) => (
                <div key={issue.id} className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm space-y-2">
                  <div className="flex items-center justify-between">
                    <span className={`text-xs px-2 py-0.5 rounded-full font-semibold ${
                      issue.status === "已報修房東" ? "bg-amber-100 text-amber-800" : "bg-red-100 text-red-800"
                    }`}>
                      {issue.status}
                    </span>
                    <span className="text-xs text-slate-400">通報者：{issue.reporter}</span>
                  </div>
                  <h3 className="font-bold text-slate-900">{issue.title}</h3>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      {/* 新增雜支彈窗 */}
      {showExpenseModal && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl max-w-sm w-full p-6 shadow-xl relative">
            <button 
              onClick={() => setShowExpenseModal(false)}
              className="absolute top-4 right-4 text-slate-400 hover:text-slate-600"
            >
              <X className="w-5 h-5" />
            </button>
            <h3 className="text-lg font-bold text-slate-900 mb-4">記錄新代墊款</h3>
            <form onSubmit={handleAddExpense} className="space-y-4">
              <div>
                <label className="text-xs font-semibold text-slate-600">購買品項</label>
                <input
                  type="text"
                  required
                  placeholder="例如：好市多洗潔精"
                  value={newExpenseTitle}
                  onChange={(e) => setNewExpenseTitle(e.target.value)}
                  className="w-full mt-1 border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-indigo-500"
                />
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-600">金額 (NT$)</label>
                <input
                  type="number"
                  required
                  placeholder="350"
                  value={newExpenseAmount}
                  onChange={(e) => setNewExpenseAmount(e.target.value)}
                  className="w-full mt-1 border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-indigo-500"
                />
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-600">代墊室友</label>
                <select
                  value={newExpensePayer}
                  onChange={(e) => setNewExpensePayer(e.target.value)}
                  className="w-full mt-1 border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-indigo-500"
                >
                  <option value="阿榮">阿榮</option>
                  <option value="柏翰">柏翰</option>
                  <option value="承恩">承恩</option>
                </select>
              </div>
              <button
                type="submit"
                className="w-full bg-indigo-600 text-white font-semibold py-2.5 rounded-xl hover:bg-indigo-700 transition mt-2 text-sm"
              >
                確認新增
              </button>
            </form>
          </div>
        </div>
      )}

      {/* 新增修繕彈窗 */}
      {showIssueModal && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl max-w-sm w-full p-6 shadow-xl relative">
            <button 
              onClick={() => setShowIssueModal(false)}
              className="absolute top-4 right-4 text-slate-400 hover:text-slate-600"
            >
              <X className="w-5 h-5" />
            </button>
            <h3 className="text-lg font-bold text-slate-900 mb-4">回報租屋處修繕</h3>
            <form onSubmit={handleAddIssue} className="space-y-4">
              <div>
                <label className="text-xs font-semibold text-slate-600">故障或維修問題</label>
                <input
                  type="text"
                  required
                  placeholder="例如：冷氣遙控器沒反應"
                  value={newIssueTitle}
                  onChange={(e) => setNewIssueTitle(e.target.value)}
                  className="w-full mt-1 border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-indigo-500"
                />
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-600">通報室友</label>
                <select
                  value={newIssueReporter}
                  onChange={(e) => setNewIssueReporter(e.target.value)}
                  className="w-full mt-1 border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-indigo-500"
                >
                  <option value="阿榮">阿榮</option>
                  <option value="柏翰">柏翰</option>
                  <option value="承恩">承恩</option>
                </select>
              </div>
              <button
                type="submit"
                className="w-full bg-indigo-600 text-white font-semibold py-2.5 rounded-xl hover:bg-indigo-700 transition mt-2 text-sm"
              >
                發布至看板
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}