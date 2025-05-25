"use client";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { useState } from "react";
import { Textarea } from "@/components/ui/textarea";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { TypographyH1 } from "@/components/ui/typography";

const formSchema = z.object({
  title: z.string(),
  description: z.string(),
  email: z.string().email(),
});

export default function ContactPage() {
  const [error, setError] = useState<string | undefined>();
  const [success, setSuccess] = useState<string | undefined>();

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      //   title: "",
      //   description: "",
      //   email: "",
    },
  });

  const onSubmit = async (values: z.infer<typeof formSchema>) => {
    setError("");
    setSuccess("");
    const msg = `TITLE: ${values.title}\nEMAIL: ${values.email}\nDESCRIPTION: ${values.description}`;
    const response = await fetch("/api/send-message", {
      method: "POST",
      body: JSON.stringify({
        msg: msg,
      }),
    });

    if (response.ok) {
      setSuccess("Mesajınız gönderildi.");
      return;
    }
    setError("Mesajınız maalesef gönderilemedi.");
    return;
  };
  return (
    <div className="py-8 px-12 flex flex-col items-center">
      <TypographyH1>İletişim</TypographyH1>
      <Form {...form}>
        <form className="space-y-8 w-3xl" onSubmit={form.handleSubmit(onSubmit)}>
          <FormField
            control={form.control}
            name="title"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Başlık</FormLabel>
                <FormControl>
                  <Input placeholder="Örnek Başlık" {...field}></Input>
                </FormControl>
                <FormDescription>Başlık Girin</FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="description"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Mesaj</FormLabel>
                <FormControl>
                  <Textarea placeholder="Örnek Mesaj" {...field} />
                </FormControl>
                <FormDescription>Mesaj girin</FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormLabel>E-posta</FormLabel>
                <FormControl>
                  <Input placeholder="Örnek E-posta" {...field} />
                </FormControl>
                <FormDescription>E-posta girin</FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
          <Button>Gönder</Button>
        </form>
      </Form>
      <div className="text-red-500">{error}</div>
      <div className="text-green-500">{success}</div>
    </div>
  );
}
