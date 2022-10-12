using System;
using System.Collections.Generic;
using System.Data;
using System.Data.Entity;
using System.Linq;
using System.Net;
using System.Web;
using System.Web.Mvc;
using electionmvc.Context;

namespace electionmvc.Controllers
{
    public class KayitOlController : Controller
    {
        private ElectionDatabaseEntities1 db = new ElectionDatabaseEntities1();

        // GET: KayitOl/Create
        public ActionResult Create()
        {
            ViewBag.SehirKod = new SelectList(db.tblSehirlers, "SehirKod", "SehirAd");
            return View();
        }

        // POST: KayitOl/Create
        // Aşırı gönderim saldırılarından korunmak için bağlamak istediğiniz belirli özellikleri etkinleştirin. 
        // Daha fazla bilgi için bkz. https://go.microsoft.com/fwlink/?LinkId=317598.
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Create([Bind(Include = "Ad,Soyad,Tc,DogumTarihi,Sifre,SehirKod")] tblKisiler tblKisiler)
        {
            if (ModelState.IsValid)
            {
                db.tblKisilers.Add(tblKisiler);
                db.SaveChanges();
                return RedirectToAction("Index","Home");
            }

            ViewBag.SehirKod = new SelectList(db.tblSehirlers, "SehirKod", "SehirAd", tblKisiler.SehirKod);
            return View(tblKisiler);
        }

        protected override void Dispose(bool disposing)
        {
            if (disposing)
            {
                db.Dispose();
            }
            base.Dispose(disposing);
        }
    }
}
