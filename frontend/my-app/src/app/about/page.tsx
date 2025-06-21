import { TypographyH1, TypographyP } from "@/components/ui/typography";

export default function AboutPage() {
  return (
    <div className="p-12">
      <TypographyH1>Hakkımızda</TypographyH1>
      <TypographyP>.</TypographyP>
      <br />
      <TypographyH1>Yasal Uyarı</TypographyH1>
      <TypographyP>
        Bu sitenin hiçbir siyasi hareket veya parti, grup, örgüt veya dernekle
        ilişkisi yoktur. Sitede yer alan içerikler sadece kamuoyunu
        bilgilendirmek amaçlıdır. Bu site 3. parti sağlayıcılardan elde ettiği
        veriyle bilgi sunmaktadır, yanlış/eksik veri olması durumunda bu site
        sorumluluk kabul etmez. Bu site hiçbir gruba, kişiye, siyasi partiye,
        kuruma, kavrama zarar verme amacı gütmez. Bu site, bu siteden kaynaklı
        herhangi bir zarardan sorumlu değildir, sorumlu tutulamaz.
        
        Kaldırılmasını istediğiniz bir içerik varsa iletişim kısmından bize yazabilirsiniz.
      </TypographyP>
    </div>
  );
}
