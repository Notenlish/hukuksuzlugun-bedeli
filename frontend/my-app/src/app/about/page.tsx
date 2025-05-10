import { TypographyH1, TypographyP } from "@/components/ui/typography";

export default function AboutPage() {
  return (
    <div className="p-12">
      <TypographyH1>About Us</TypographyH1>
      <TypographyP>
        Lorem ipsum dolor sit, amet consectetur adipisicing elit. Assumenda sint expedita
        numquam animi fuga obcaecati omnis provident exercitationem corrupti, eum, enim
        ipsum dolore labore perferendis autem voluptas voluptate officiis molestiae.
      </TypographyP>
      <br />
      <TypographyH1>Disclaimer</TypographyH1>
      <TypographyP>
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Qui dolore odit aut
        ducimus. Odio iusto fugit in, culpa vel eaque, impedit neque, commodi numquam ab
        praesentium repellendus obcaecati velit explicabo.
      </TypographyP>
    </div>
  );
}
