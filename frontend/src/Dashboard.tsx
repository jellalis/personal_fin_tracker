import { useEffect, useMemo, useState } from "react";
import {
  TrendingUp,
  TrendingDown,
  Plus,
  Trash2,
  UtensilsCrossed,
  Train,
  ShoppingBag,
  Swords,
  Receipt,
  Coins,
  HelpCircle,
  Scroll,
  LogOut,
} from "lucide-react";
import { api, type Category, type Transaction } from "./api";

// ---------------------------------------------------------------------------
// Asset paths — replace with your own images or use the originals from the
// Lovable project's src/assets/ folder.
// ---------------------------------------------------------------------------
const ASSET = {
  gamaWallet: "/assets/gama-wallet.webp",   // toad wallet mascot
  narutoGama: "/assets/naruto-gama.webp",   // naruto + gama-chan header icon
  budget25:   "/assets/budget-25.png",
  budget50:   "/assets/budget-50.png",
  budget75:   "/assets/budget-75.png",
  budget100:  "/assets/budget-100.png",
};

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------
const BUDGET_TIERS = [
  { pct: 25,  src: ASSET.budget25,  label: "Plump purse",    jp: "余裕", tone: "text-leaf" },
  { pct: 50,  src: ASSET.budget50,  label: "Halfway gone",   jp: "半分", tone: "text-gold" },
  { pct: 75,  src: ASSET.budget75,  label: "Getting nervous",jp: "危機", tone: "text-ember" },
  { pct: 100, src: ASSET.budget100, label: "Broke shinobi",  jp: "破産", tone: "text-destructive" },
] as const;

const CATEGORY_META: Record<
  Category,
  { label: string; jp: string; icon: React.ComponentType<{ className?: string }>; tone: string }
> = {
  food:          { label: "Ramen",    jp: "食", icon: UtensilsCrossed, tone: "bg-toad/25" },
  transport:     { label: "Travel",   jp: "旅", icon: Train,           tone: "bg-leaf/20" },
  shopping:      { label: "Market",   jp: "店", icon: ShoppingBag,     tone: "bg-gold/30" },
  entertainment: { label: "Training", jp: "技", icon: Swords,          tone: "bg-ember/20" },
  bills:         { label: "Tribute",  jp: "税", icon: Receipt,         tone: "bg-muted" },
  salary:        { label: "Mission",  jp: "任", icon: Coins,           tone: "bg-leaf/25" },
  other:         { label: "Other",    jp: "他", icon: HelpCircle,      tone: "bg-muted" },
};

function formatRyo(n: number, currency = "USD") {
  return new Intl.NumberFormat("en-US", { style: "currency", currency }).format(n);
}

// ---------------------------------------------------------------------------
// Main Dashboard component
// Drop this anywhere in your app: <Dashboard />
// ---------------------------------------------------------------------------
export function Dashboard({ onLogout }: { onLogout: () => void }) {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [currency, setCurrency] = useState("EUR");
  const [loading, setLoading] = useState(true);

  // Load real data from the backend on mount
  useEffect(() => {
    Promise.all([api.listTransactions(), api.getSummary()])
      .then(([txs, summary]) => {
        setTransactions(txs);
        setCurrency(summary.currency);
      })
      .finally(() => setLoading(false));
  }, []);

  // Compute summary locally from loaded transactions (stays in sync with adds/deletes)
  const summary = useMemo(() => {
    const income  = transactions.filter((t) => t.amount > 0).reduce((s, t) => s + t.amount, 0);
    const expense = transactions.filter((t) => t.amount < 0).reduce((s, t) => s + Math.abs(t.amount), 0);
    return { balance: income - expense, income, expense, currency };
  }, [transactions, currency]);

  const maxExpense = Math.max(...transactions.map((t) => Math.abs(t.amount)), 1);

  if (loading) {
    return (
      <main className="min-h-screen flex items-center justify-center">
        <p className="font-display text-2xl animate-pulse">Summoning data...</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen px-4 py-8 md:px-10 md:py-12">
      {/* faint kanji watermark */}
      <div
        aria-hidden
        className="pointer-events-none fixed inset-0 flex items-center justify-center overflow-hidden"
      >
        <span className="font-display select-none text-[40vw] leading-none text-ink/[0.03]">忍</span>
      </div>

      <div className="relative mx-auto max-w-6xl">

        {/* ── Header ────────────────────────────────────────────────────── */}
        <header className="mb-8 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="stamp flex h-12 w-12 items-center justify-center bg-primary text-primary-foreground">
              <span className="font-display text-2xl">蛙</span>
            </div>
            <div>
              <h1 className="font-display text-2xl leading-none md:text-3xl">
                Gama Wallet <span className="text-ember">・</span> ガマ財布
              </h1>
              <p className="text-xs text-muted-foreground md:text-sm">
                The toad sannin's coin purse — for shinobi on a budget
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="hanko hidden items-center gap-2 px-3 py-1 text-sm md:inline-flex">
              <img
                src={ASSET.narutoGama}
                alt="Naruto holding Gama-chan"
                className="h-8 w-8 rounded-full border-2 border-ink object-cover"
              />
              FastAPI 巻
            </span>
            <button
              onClick={onLogout}
              title="Logout"
              className="stamp p-2 hover:bg-muted text-muted-foreground hover:text-destructive transition-colors"
            >
              <LogOut className="h-4 w-4" />
            </button>
          </div>
        </header>

        {/* ── HERO — balance summary ─────────────────────────────────────── */}
        <section
          className="scroll-card relative mb-8 overflow-hidden p-6 md:p-10"
          style={{ background: "var(--gradient-hero)" }}
        >
          <span className="absolute inset-x-0 top-0 h-2 bg-ink" />
          <span className="absolute inset-x-0 bottom-0 h-2 bg-ink" />

          <div className="grid items-center gap-6 md:grid-cols-[1.5fr_1fr]">
            <div className="text-primary-foreground">
              <span className="stamp inline-block bg-scroll px-3 py-1 text-xs font-semibold uppercase tracking-widest text-ink">
                Mission Report ✦ 任務報告
              </span>
              <h2 className="font-display mt-4 text-3xl md:text-5xl">Coin Purse Balance</h2>
              <p className="font-display mt-2 text-4xl md:text-6xl drop-shadow-[2px_2px_0_rgba(0,0,0,0.35)]">
                {formatRyo(summary.balance, summary.currency)}
              </p>
              <div className="mt-5 flex flex-wrap gap-3">
                <StatBadge
                  icon={<TrendingUp className="h-4 w-4" />}
                  label="Earned"
                  value={formatRyo(summary.income, summary.currency)}
                  tone="bg-leaf text-primary-foreground"
                />
                <StatBadge
                  icon={<TrendingDown className="h-4 w-4" />}
                  label="Spent"
                  value={formatRyo(summary.expense, summary.currency)}
                  tone="bg-ink text-primary-foreground"
                />
              </div>
            </div>

            <div className="relative mx-auto h-48 w-48 md:h-64 md:w-64">
              <span className="animate-coin absolute -left-2 top-4 text-3xl">🪙</span>
              <span className="animate-coin absolute right-0 top-10 text-2xl" style={{ animationDelay: "1s" }}>🪙</span>
              <img
                src={ASSET.gamaWallet}
                alt="Gama-chan the toad wallet"
                className="animate-float h-full w-full object-contain drop-shadow-[6px_6px_0_rgba(0,0,0,0.35)]"
              />
            </div>
          </div>
        </section>

        {/* ── Budget Chakra — progress + tier cards ─────────────────────── */}
        <BudgetChakra income={summary.income} expense={summary.expense} />

        <section className="grid gap-6 lg:grid-cols-[1.4fr_1fr]">

          {/* ── Mission Ledger — transaction list ───────────────────────── */}
          <div className="scroll-card p-6">
            <div className="mb-5 flex items-center justify-between border-b-2 border-dashed border-ink/40 pb-3">
              <h3 className="font-display flex items-center gap-2 text-xl">
                <Scroll className="h-5 w-5" /> Mission Ledger
              </h3>
              <button
                onClick={() => setShowForm((s) => !s)}
                className="stamp stamp-hover inline-flex items-center gap-2 bg-primary px-3 py-1.5 text-sm font-semibold text-primary-foreground"
              >
                <Plus className="h-4 w-4" /> Log entry
              </button>
            </div>

            {showForm && (
              <AddForm
                onAdd={async (tx) => {
                  const created = await api.createTransaction(tx);
                  setTransactions((prev) => [created, ...prev]);
                  setShowForm(false);
                }}
                onCancel={() => setShowForm(false)}
              />
            )}

            <ul className="space-y-3">
              {transactions.map((tx) => {
                const meta    = CATEGORY_META[tx.category];
                const Icon    = meta.icon;
                const isIncome = tx.amount > 0;
                return (
                  <li key={tx.id} className="stamp flex items-center justify-between gap-3 bg-card p-3">
                    <div className="flex min-w-0 items-center gap-3">
                      <div className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-md border-2 border-ink ${meta.tone}`}>
                        <Icon className="h-5 w-5" />
                      </div>
                      <div className="min-w-0">
                        <p className="truncate font-semibold">{tx.title}</p>
                        <p className="text-xs text-muted-foreground">
                          <span className="font-display mr-1 text-ember">{meta.jp}</span>
                          {meta.label} · {new Date(tx.date).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`font-display text-base md:text-lg ${isIncome ? "text-leaf" : "text-ember"}`}>
                        {isIncome ? "+" : "−"}{formatRyo(Math.abs(tx.amount), summary.currency)}
                      </span>
                      <button
                        aria-label={`Delete ${tx.title}`}
                        onClick={async () => {
                          await api.deleteTransaction(tx.id);
                          setTransactions((prev) => prev.filter((t) => t.id !== tx.id));
                        }}
                        className="rounded-md p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-destructive"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </li>
                );
              })}
            </ul>
          </div>

          <div className="space-y-6">
            {/* ── Chakra Spending — top-5 expense bars ──────────────────── */}
            <ChakraSpending transactions={transactions} maxExpense={maxExpense} currency={summary.currency} />

            {/* ── API reference card ────────────────────────────────────── */}
            <div className="scroll-card bg-ink p-6 text-scroll">
              <h3 className="font-display mb-2 text-xl text-primary">Summoning Scroll 召喚の術</h3>
              <p className="mb-4 text-sm opacity-80">
                Set{" "}
                <code className="rounded bg-scroll px-1.5 py-0.5 text-xs text-ink">VITE_API_URL</code>
                {" "}and implement these FastAPI routes:
              </p>
              <ul className="space-y-1.5 font-mono text-xs">
                <li className="stamp bg-scroll px-3 py-1.5 text-ink">GET  /summary</li>
                <li className="stamp bg-scroll px-3 py-1.5 text-ink">GET  /transactions</li>
                <li className="stamp bg-scroll px-3 py-1.5 text-ink">POST /transactions</li>
                <li className="stamp bg-scroll px-3 py-1.5 text-ink">DELETE /transactions/&#123;id&#125;</li>
              </ul>
            </div>
          </div>
        </section>

        <footer className="mt-10 text-center text-xs text-muted-foreground">
          一銭を笑う者は一銭に泣く · "He who laughs at a single coin will cry for one."
        </footer>
      </div>
    </main>
  );
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function BudgetChakra({ income, expense }: { income: number; expense: number }) {
  const usagePct = income > 0 ? Math.min(100, Math.round((expense / income) * 100)) : 0;
  const activeTier = BUDGET_TIERS.reduce((prev, t) =>
    Math.abs(t.pct - usagePct) < Math.abs(prev.pct - usagePct) ? t : prev
  , BUDGET_TIERS[0]);

  return (
    <section className="scroll-card mb-8 p-6 md:p-8">
      <div className="mb-5 flex flex-wrap items-end justify-between gap-3 border-b-2 border-dashed border-ink/40 pb-3">
        <div>
          <h3 className="font-display text-xl">Budget Chakra 予算</h3>
          <p className="text-xs text-muted-foreground">Your wallet's mood — based on spent vs. earned.</p>
        </div>
        <div className="text-right">
          <p className={`font-display text-3xl md:text-4xl ${activeTier.tone}`}>{usagePct}%</p>
          <p className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">
            {activeTier.jp} · {activeTier.label}
          </p>
        </div>
      </div>

      {/* progress bar */}
      <div className="mb-6 h-4 overflow-hidden rounded-sm border-2 border-ink bg-muted">
        <div
          className="h-full transition-all"
          style={{ width: `${usagePct}%`, background: "var(--gradient-ember)" }}
        />
      </div>

      {/* tier cards */}
      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        {BUDGET_TIERS.map((tier) => {
          const isActive = tier.pct === activeTier.pct;
          return (
            <figure
              key={tier.pct}
              className={`stamp overflow-hidden bg-card transition-all ${
                isActive
                  ? "scale-[1.03] ring-4 ring-primary"
                  : "opacity-50 grayscale hover:opacity-80 hover:grayscale-0"
              }`}
            >
              <img
                src={tier.src}
                alt={`${tier.pct}% budget used — ${tier.label}`}
                className="aspect-[4/3] w-full object-cover"
              />
              <figcaption className="flex items-center justify-between border-t-2 border-ink bg-scroll px-3 py-2">
                <span className={`font-display text-lg ${tier.tone}`}>{tier.pct}%</span>
                <span className="text-xs font-semibold">
                  <span className="font-display mr-1 text-ember">{tier.jp}</span>
                  {tier.label}
                </span>
              </figcaption>
            </figure>
          );
        })}
      </div>
    </section>
  );
}

function ChakraSpending({
  transactions,
  maxExpense,
  currency,
}: {
  transactions: Transaction[];
  maxExpense: number;
  currency: string;
}) {
  const expenses = transactions.filter((t) => t.amount < 0).slice(0, 5);

  return (
    <div className="scroll-card p-6">
      <h3 className="font-display mb-4 text-xl">Chakra Spending 消費</h3>
      <div className="space-y-3">
        {expenses.map((t) => {
          const meta = CATEGORY_META[t.category];
          const pct  = (Math.abs(t.amount) / maxExpense) * 100;
          return (
            <div key={t.id}>
              <div className="mb-1 flex justify-between text-xs">
                <span className="font-medium">
                  <span className="font-display mr-1 text-ember">{meta.jp}</span>
                  {meta.label}
                </span>
                <span className="text-muted-foreground">
                  {formatRyo(Math.abs(t.amount), currency)}
                </span>
              </div>
              <div className="h-3 overflow-hidden rounded-sm border-2 border-ink bg-muted">
                <div
                  className="h-full"
                  style={{ width: `${pct}%`, background: "var(--gradient-ember)" }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function StatBadge({
  icon, label, value, tone,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  tone: string;
}) {
  return (
    <div className={`stamp flex items-center gap-2 px-3 py-2 ${tone}`}>
      {icon}
      <div className="flex flex-col leading-tight">
        <span className="text-[10px] font-semibold uppercase tracking-widest opacity-80">{label}</span>
        <span className="font-display text-sm">{value}</span>
      </div>
    </div>
  );
}

function AddForm({
  onAdd,
  onCancel,
}: {
  onAdd: (tx: Omit<Transaction, "id">) => void;
  onCancel: () => void;
}) {
  const [title,    setTitle]    = useState("");
  const [amount,   setAmount]   = useState("");
  const [category, setCategory] = useState<Category>("food");
  const [type,     setType]     = useState<"expense" | "income">("expense");

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        const n = parseFloat(amount);
        if (!title || isNaN(n)) return;
        onAdd({
          title,
          amount: type === "expense" ? -Math.abs(n) : Math.abs(n),
          category,
          date: new Date().toISOString().slice(0, 10),
        });
      }}
      className="stamp mb-4 grid gap-3 bg-muted/60 p-4 md:grid-cols-2"
    >
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Mission name…"
        className="stamp bg-card px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-ring md:col-span-2"
      />
      <input
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        type="number"
        step="0.01"
        placeholder="Ryo amount"
        className="stamp bg-card px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-ring"
      />
      <select
        value={category}
        onChange={(e) => setCategory(e.target.value as Category)}
        className="stamp bg-card px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-ring"
      >
        {Object.entries(CATEGORY_META).map(([k, v]) => (
          <option key={k} value={k}>{v.jp} {v.label}</option>
        ))}
      </select>
      <div className="flex gap-2 md:col-span-2">
        <button
          type="button"
          onClick={() => setType("expense")}
          className={`stamp flex-1 px-3 py-2 text-sm font-semibold ${type === "expense" ? "bg-ember text-primary-foreground" : "bg-card"}`}
        >
          − Spend
        </button>
        <button
          type="button"
          onClick={() => setType("income")}
          className={`stamp flex-1 px-3 py-2 text-sm font-semibold ${type === "income" ? "bg-leaf text-primary-foreground" : "bg-card"}`}
        >
          + Earn
        </button>
      </div>
      <div className="flex gap-2 md:col-span-2">
        <button
          type="submit"
          className="stamp stamp-hover flex-1 bg-primary px-3 py-2 text-sm font-semibold text-primary-foreground"
        >
          Seal it 封
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="stamp bg-card px-3 py-2 text-sm font-semibold"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}
