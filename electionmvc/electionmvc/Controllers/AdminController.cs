using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using electionmvc.Context;

namespace electionmvc.Controllers
{
    public class AdminController : Controller
    {
        // GET: Admin
        private ElectionDatabaseEntities1 db = new ElectionDatabaseEntities1();
        
        public ActionResult Index()
        {
            return View(db.tblKisilers.ToList());
        }

        public ActionResult SecimEkle()
        {
            return View();
        }

        [HttpPost]
        public ActionResult SecimEkle([Bind(Include = "secimAd,secimTarihi,secimSonTarihi")] tblSecim tblsecim)
        {
            if (ModelState.IsValid)
            {
                db.tblSecims.Add(tblsecim);
                db.SaveChanges();
                return RedirectToAction("Index", "Admin");
            }

            return View(tblsecim);
        }

        public ActionResult AdayEkle()
        {
            ViewBag.kisilerID = new SelectList(db.tblKisilers.Where(m => m.Tc != "11111111111"), "kisilerID", "Tc");
            ViewBag.secimID = new SelectList(db.tblSecims, "secimID", "secimAd");
            return View();
        }

        [HttpPost]
        public ActionResult AdayEkle([Bind(Include = "adayID,secimID,kisilerID")] tblAdaylar tblAdaylar)
        {
            if(ModelState.IsValid)
            {
                db.tblAdaylars.Add(tblAdaylar);
                db.SaveChanges();
                return RedirectToAction("Index");
            }
            ViewBag.kisilerID = new SelectList(db.tblKisilers, "kisilerID", "Ad", tblAdaylar.kisilerID);
            ViewBag.secimID = new SelectList(db.tblSecims, "secimID", "secimAd", tblAdaylar.secimID);
            return View(tblAdaylar);
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