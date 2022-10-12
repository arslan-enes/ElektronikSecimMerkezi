using electionmvc.Context;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Web.UI;
using RestSharp;

namespace electionmvc.Controllers
{
    public class LoginController : Controller
    {
        // GET: Login
        public ActionResult Index()
        {
            Session["userID"] = null;
            Session["userFirstName"] = null;
            Session["userLastName"] = null;
            return View();
        }
        [HttpPost]
        public ActionResult Authorize(electionmvc.Context.tblKisiler userModel)
        {
            
            using (ElectionDatabaseEntities1 db = new ElectionDatabaseEntities1())
            {
                var userDetails = db.tblKisilers.Where(x => x.Tc == userModel.Tc && x.Sifre == userModel.Sifre).FirstOrDefault();
                using (ServiceReference1.KPSPublicSoapClient tc = new ServiceReference1.KPSPublicSoapClient())
                {
                    bool sonuc = tc.TCKimlikNoDogrula(Convert.ToInt64(userDetails.Tc), userDetails.Ad, userDetails.Soyad, userDetails.DogumTarihi.Year);
                }
                if (userDetails!=null)
                {                    
                    string tcno, sifre;
                    tcno = userDetails.Tc;
                    sifre = userDetails.Sifre;
                  
                    if (tcno == "11111111111" && sifre == "Admin123")
                    {
                        Session["userID"] = userDetails.kisilerID;
                        Session["userFirstName"] = userDetails.Ad;
                        Session["userLastName"] = userDetails.Soyad;
                        return RedirectToAction("Index", "Admin");
                    }
                    else
                    {
                        
                        Session["userID"] = userDetails.kisilerID;
                        Session["userFirstName"] = userDetails.Ad;
                        Session["userLastName"] = userDetails.Soyad;
                        
                        return RedirectToAction("Index", "Secmen");
                    }
                }
                else
                {
                    return View("Index", userModel);
                }           
            }
        }
    }
}