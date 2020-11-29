#![feature(proc_macro_hygiene, decl_macro)]
#[macro_use] extern crate rocket;

#[get("/")]
fn index() -> &'static str {
    "Hello, world!"
}

#[get("/about")]
fn about() -> String {
    return format!("link for");
}

#[get("/l/<shortlink>")]
fn redirect(shortlink: String) -> String {
    return format!("link for {}", shortlink);
}

#[get("/shortlinks")]
fn shortlinks() -> String {
    return format!("link for");
}

#[post("/shortlinks")]
fn linkpost() -> String {
    return format!("post thiz lelz");
}

#[get("/shortlinks/<id>/delete")]
fn delete_shortlink(id: String) -> String {
    return format!("link for");
}

fn main() {
    rocket::ignite()
        .mount("/", routes![
            index, 
            redirect, 
            shortlinks, 
            linkpost])
    .launch();
}