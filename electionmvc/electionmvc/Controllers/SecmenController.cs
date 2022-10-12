using System;
using System.Collections.Generic;
using System.Data;
using System.Data.Entity;
using System.Linq;
using System.Net;
using System.Web;
using System.Web.Mvc;
using electionmvc.Context;
using System.Net.Http;
using RestSharp;

namespace electionmvc.Controllers
{
    public class SecmenController : Controller
    {
        // GET: Secmen
        private ElectionDatabaseEntities1 db = new ElectionDatabaseEntities1();

        public ActionResult Index()
        {
            var sonuc = from secim in db.tblSecims
                        where secim.secimSonTarihi > DateTime.Now && secim.secimTarihi <= DateTime.Now
                        select secim;
            
            return View(sonuc.ToList());
            
        }
        public ActionResult GelecekSecimler()
        {
            var sonuc = from secim in db.tblSecims
                        where secim.secimTarihi > DateTime.Now
                        select secim;


            return View(sonuc.ToList());
        }


        public ActionResult GecmisSecimler()
        {
            return View(db.GecmisSecimlers.ToList());
        }
        public ActionResult Sandik(int? id)
        {
            if (id == null)
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }
            tblSecim tblsecim = db.tblSecims.Find(id);
            if (tblsecim == null)
            {
                return HttpNotFound();
            }
            ViewBag.secimID = new SelectList(db.Secimlers,"secimID","secimAd", tblsecim.secimID);
            var adaylar = from aday in db.tblAdaylars
                          where aday.secimID == tblsecim.secimID
                          select aday;
            return View(adaylar);
        }

        [HttpPost]
        public ActionResult Index(int? id)
        {

            

            string query = "update tblAdaylar set AlinanOy +=1 where adayID =" + id;
            db.Database.ExecuteSqlCommand(query);
            
            tblAdaylar aday = (from p in db.tblAdaylars
                               where p.adayID == id
                               select p).SingleOrDefault();



            var client = new RestClient("http://127.0.0.1:5000/");
            // client.Authenticator = new HttpBasicAuthenticator(username, password);
            var request = new RestRequest("createBlock/");
            request.RequestFormat = DataFormat.Json;
            request.AddJsonBody(new { data = aday.tblKisiler.Ad + aday.tblKisiler.Soyad + aday.adayID + Session["userID"]}); // Anonymous type object is converted to Json bodyx
            var response = client.Post(request);
            var content = response.Content; // Raw content as string
            System.Diagnostics.Debug.WriteLine(content);

            Session["selectionID"] = aday.secimID.ToString();
            Session["oyveren"] = Session["userID"];


            return RedirectToAction("Index");
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