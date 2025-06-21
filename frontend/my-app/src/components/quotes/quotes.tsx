import Quote from "@/components/quotes/quote";

import { QuoteData } from "@/types";
const quoteData: QuoteData[] = [
  {
    author:
      "Türkiye Odalar ve Borsalar Birliği (TOBB) Başkanı Rifat Hisarcıklıoğlu",
    text: "Kredilerdeki daralma ve yüksek faiz oranları, özellikle KOBİ’lerimizin ayağına pranga oluyor. KOBİ’lere pozitif ayrımcılık yapmalıyız.",
    image: "/rifat-hisarciklioglu.webp",
    date: new Date(2025, 5, 17),
    source:
      "https://bigpara.hurriyet.com.tr/haberler/ekonomi-haberleri/is-dunyasindan-finansman-cagrisi_ID1611859/",
  },
  {
    author:"Türkiye Odalar ve Borsalar Birliği (TOBB) Başkanı Rifat Hisarcıklıoğlu",
    image:"/rifat-hisarciklioglu.webp",
    text:"Vergi denetimine karşı değiliz. Kayıtdışı ekonomiyle mücadeleyi destekliyoruz. Vergi sistemi adil ve şeffaf olmalı. Girişimcinin çalışma şevkini kırmamalı. Her işletmenin, her fabrikanın kapısına vergi memuru koyarak, polisiye tedbirler alarak, vergi gelirleri arttırılamaz. Hakkaniyet de sağlanamaz.",
    date:new Date(2025, 5, 6),
    source:"https://halktv.com.tr/siyaset/tobb-baskani-rifat-hisarciklioglu-mehmet-simseke-isyan-bayragini-cekti-935956h"
  },
  {
    author:"İstanbul Ticaret Odası (İTO) Başkanı Şekib Avdagiç",
    source:"https://www.bloomberght.com/ito-dan-faiz-aciklamasi-3750446?page=2",
    text:"Türkiye yılda en az yüzde 4,5-5 bandında büyümeli. Bunun için de gerekli adımların üçüncü ve dördüncü çeyrekte atılmasını bekliyoruz. Dolayısıyla, enflasyonun bir an önce kalıcı olarak tek haneye indirilmesi ve buna bağlı olarak da 'üretimi, yatırımı, istihdamı' baskılayan yüksek faiz ortamının sonlandırılması büyük önem taşıyor.",
    date:new Date(2025, 6, 13),
    image:"/sekib-avdagic.jpeg"
  },
  {
    author:"İstanbul Sanayi Odası Başkanı Erdal Bahçıvan",
    source:"https://www.patronlardunyasi.com/istanbul-sanayi-odasi-baskani-erdal-bahcivan-yuksek-faiz-ortaminda-en-buyuk-bedeli-sanayici-oduyor",
    date:new Date(2024, 11, 5),
    text:"Şu anda en başta yüksek faiz ortamı çözüm noktasındaki en büyük problem. Faizin düşmesinin de yegane şartı enflasyonun düşmesi. Yumurta-tavuk, tavuk-yumurta ikilemin içerisinde. Yüksek faiz ortamında en büyük bedeli sanayici ödüyor.",
    image:"/erdal-bahcivan.jpg"
  }
];

export default function Quotes() {
  return quoteData.sort((a,b) => b.date.valueOf()-a.date.valueOf()).map((q, i) => <Quote key={i} quoteData={q}></Quote>);
}
