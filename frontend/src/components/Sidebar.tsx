import React from "react";

import { 
  Drawer,
  AppBar,
  Box,
  Divider,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  Typography,
  ListItemIcon,
  Toolbar,
  ListItemText,
  CssBaseline
} from "@mui/material";

import { useNavigate } from "react-router-dom";

import MailIcon from "@mui/icons-material/Mail";
import MenuIcon from "@mui/icons-material/Menu";
import LibraryBooksIcon from "@mui/icons-material/LibraryBooks";
import HistoryIcon from "@mui/icons-material/History";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import CreateIcon from "@mui/icons-material/Create";
import Logo from "./Logo";
import LogoutButton from "./LogoutButton";

const drawerWidth = 240;

interface Props {
  window?: () => Window;
}

const Sidebar = (props : Props)  => {
  const { window } = props;
  const [mobileOpen, setMobileOpen] = React.useState(false);

  const navigate = useNavigate();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const drawer = (
    <Box>
      {/* <Toolbar /> */}
      <Box sx={{ display: "flex", justifyContent: "center" }}>
        <Logo/>
      </Box>
      <Divider />
      <List>

        <ListItem key="join-link" disablePadding>
          <ListItemButton onClick={() => navigate("/")}>
            <ListItemIcon>
              <AddCircleOutlineIcon/>
            </ListItemIcon>
            <ListItemText primary="Join Comp" />
          </ListItemButton>
        </ListItem>

        <ListItem key="create-link" disablePadding>
          <ListItemButton onClick={() => navigate("/competitions/create")}>
            <ListItemIcon>
              <CreateIcon/>
            </ListItemIcon>
            <ListItemText primary="Create Comp" />
          </ListItemButton>
        </ListItem>


      </List>
      <Divider />
      <List>
        <ListItem key="recent-link" disablePadding>
          <ListItemButton onClick={() => navigate("/competitions/list/all")}>
            <ListItemIcon>
              <LibraryBooksIcon/>
            </ListItemIcon>
            <ListItemText primary="Your Comps" />
          </ListItemButton>
        </ListItem>

        {/* <ListItem key="completed-link" disablePadding>
          <ListItemButton>
            <ListItemIcon>
              <HistoryIcon/>
            </ListItemIcon>
            <ListItemText primary="Completed Games" />
          </ListItemButton>
        </ListItem> */}
      </List>
    </Box>
  );

  const container = window !== undefined ? () => window().document.body : undefined;

  return (
    <Box sx={{ display: "flex" }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        <Toolbar
          sx={{
            display: "flex",
          }}
        >
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: "none" } }}
          >
            <MenuIcon />
          </IconButton>

          <Box
            sx={{
              display: "flex",
              flexGrow: 1,
              justifyContent: "flex-end"
            }}
          >
            <LogoutButton/>
          </Box>
          {/* <Typography variant="h6" noWrap component="div">
            Responsive drawer!!
          </Typography> */}

        </Toolbar>
      </AppBar>
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 }}}
        aria-label="Menu Options"
      >
        {/* The implementation can be swapped with js to avoid SEO duplication of links. */}
        <Drawer
          container={container}
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile.
          }}
          sx={{
            display: { xs: "block", sm: "none" },
            "& .MuiDrawer-paper": { boxSizing: "border-box", width: drawerWidth },
            bgcolor: "pallete.primary.dark"
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: "none", sm: "block" },
            "& .MuiDrawer-paper": { boxSizing: "border-box", width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
    </Box>
  );
};

export default Sidebar;