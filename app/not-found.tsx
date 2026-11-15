import Link from "next/link";

export default function NotFound() {
  return (
    <div className="gut">
      <div className="wrap main">
        <div className="empty">
          <strong>Bunday sahifa topilmadi</strong>
          Manzil o‘zgargan bo‘lishi mumkin. <Link href="/">Bosh sahifaga qaytib</Link>, kerakli maslahatni qidiruv orqali toping.
        </div>
      </div>
    </div>
  );
}
