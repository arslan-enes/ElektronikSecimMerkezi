//------------------------------------------------------------------------------
// <auto-generated>
//     This code was generated from a template.
//
//     Manual changes to this file may cause unexpected behavior in your application.
//     Manual changes to this file will be overwritten if the code is regenerated.
// </auto-generated>
//------------------------------------------------------------------------------

namespace electionmvc.Context
{
    using System;
    using System.Collections.Generic;
    
    public partial class tblSecim
    {
        [System.Diagnostics.CodeAnalysis.SuppressMessage("Microsoft.Usage", "CA2214:DoNotCallOverridableMethodsInConstructors")]
        public tblSecim()
        {
            this.tblAdaylars = new HashSet<tblAdaylar>();
        }
    
        public int secimID { get; set; }
        public string secimAd { get; set; }
        public System.DateTime secimTarihi { get; set; }
        public System.DateTime secimSonTarihi { get; set; }
    
        [System.Diagnostics.CodeAnalysis.SuppressMessage("Microsoft.Usage", "CA2227:CollectionPropertiesShouldBeReadOnly")]
        public virtual ICollection<tblAdaylar> tblAdaylars { get; set; }
    }
}
