#![feature(proc_macro_hygiene, decl_macro)]
#[macro_use] extern crate rocket;

#[get("/")]
fn index() -> &'static str {
    "Hello, world!"
}

#[get("/l/<shortlink>")]
fn redirect(shortlink: String) -> String {
    return format!("link for {}", shortlink);
}

#[get("/links")]
fn links() -> String {
    return format!("link for");
}

#[post("/links")]
fn linkpost() -> String {
    return format!("post thiz lelz");
}

fn main() {
    rocket::ignite()
        .mount("/", routes![
            index, 
            redirect, 
            links, 
            linkpost])
    .launch();
}